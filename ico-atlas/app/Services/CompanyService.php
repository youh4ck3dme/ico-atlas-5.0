<?php

namespace App\Services;

use App\Services\Company\Providers\OrsrProvider;
use App\Services\Company\Providers\ZrsrProvider;
use App\Services\Company\Providers\RuzProvider;
use App\Services\RegionResolver;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class CompanyService
{
    public function __construct(
        private OrsrProvider $orsr,
        private ZrsrProvider $zrsr,
        private RuzProvider $ruz,
        private RegionResolver $regionResolver,
    ) {
    }

    /**
     * Hlavný vstup pre lookup podľa IČO.
     *
     * @return array{
     *   data: array{
     *     ico: string,
     *     name: string|null,
     *     dic: string|null,
     *     ic_dph: string|null,
     *     legal_form: string|null,
     *     address: string|null,
     *     city: string|null,
     *     zip: string|null,
     *     district: string|null,
     *     region: string|null,
     *     country: string|null,
     *     source: string|null,
     *   },
     *   meta: array{
     *     cached: bool,
     *     latency_ms: int,
     *   }
     * }
     */
    public function lookupByIco(string $ico): array
    {
        $cacheKey = "icoatlas:company:{$ico}";
        $start = microtime(true);

        // 0) Cache check
        if (Cache::has($cacheKey)) {
            $cached = Cache::get($cacheKey);
            $latencyMs = (int) ((microtime(true) - $start) * 1000);

            return [
                'data' => $this->normalizeCompanyArray($cached),
                'meta' => [
                    'cached'     => true,
                    'latency_ms' => $latencyMs,
                ],
            ];
        }

        // 1) ORSR je primárny zdroj štruktúry
        $company = $this->fromOrsr($ico);

        // 2) ZRSR / RÚZ – enrichment DIC / IČ DPH, ak chýbajú
        $company = $this->enrichTaxIds($ico, $company);

        // 3) Ak nič, "not-found" štruktúra (stále drží 12 polí)
        if (!$company) {
            $company = $this->emptyCompany($ico);
        }

        // 4) PSČ → okres / kraj
        if (!empty($company['zip']) && empty($company['district']) && empty($company['region'])) {
            $resolved = $this->regionResolver->fromZip($company['zip']);

            $company['district'] = $company['district'] ?? $resolved['district'];
            $company['region']   = $company['region']   ?? $resolved['region'];
        }

        // 5) Fallback country, ak by nebolo
        if (empty($company['country'])) {
            $company['country'] = 'SK';
        }

        // 6) Cache s TTL
        Cache::put(
            $cacheKey,
            $company,
            now()->addHours((int) config('icoatlas.cache_ttl_hours', 12))
        );

        $latencyMs = (int) ((microtime(true) - $start) * 1000);

        Log::channel('icoatlas')->info('icoatlas.lookup', [
            'ico'        => $ico,
            'source'     => $company['source'] ?? null,
            'cached'     => false,
            'latency_ms' => $latencyMs,
        ]);

        return [
            'data' => $this->normalizeCompanyArray($company),
            'meta' => [
                'cached'     => false,
                'latency_ms' => $latencyMs,
            ],
        ];
    }

    /**
     * ORSR → core dáta.
     *
     * @return array<string, mixed>|null
     */
    private function fromOrsr(string $ico): ?array
    {
        try {
            $raw = $this->orsr->getDetailByIco($ico);

            if (!$raw) {
                return null;
            }

            // Mapa z ORSR štruktúry na kontrakt 12 polí
            return [
                'ico'        => $ico,
                'name'       => $raw['name']        ?? null,
                'dic'        => $raw['dic']         ?? null, // ak by náhodou niekedy bolo
                'ic_dph'     => $raw['ic_dph']      ?? null,
                'legal_form' => $raw['legal_form']  ?? null,
                'address'    => $raw['street']      ?? $raw['address'] ?? null,
                'city'       => $raw['city']        ?? null,
                'zip'        => $raw['zip']         ?? null,
                'district'   => $raw['district']    ?? null,
                'region'     => $raw['region']      ?? null,
                'country'    => $raw['country']     ?? 'SK',
                'source'     => 'orsr',
            ];

        } catch (\Throwable $e) {
            Log::channel('icoatlas')->error('orsr.lookup.error', [
                'ico'   => $ico,
                'error' => $e->getMessage(),
            ]);

            return null;
        }
    }

    /**
     * Enrichment DIC / IČ DPH zo ZRSR a RÚZ.
     *
     * Priority:
     *  1. Ak už máme dic/ic_dph z ORSR → neprepíname.
     *  2. Ak chýba, skúšame ZRSR.
     *  3. Ak stále chýba, skúšame RÚZ.
     *
     * @param array<string, mixed>|null $company
     * @return array<string, mixed>|null
     */
    private function enrichTaxIds(string $ico, ?array $company): ?array
    {
        if (!$company) {
            // Nemáme ani ORSR, ale aj tak môžeme skúsiť ZRSR/RÚZ
            $company = $this->emptyCompany($ico);
            $company['source'] = 'not-found'; // zatiaľ
        }

        $hasDic   = !empty($company['dic']);
        $hasIcdph = !empty($company['ic_dph']);

        if ($hasDic && $hasIcdph) {
            return $company;
        }

        // 1) ZRSR
        try {
            $zrsr = $this->zrsr->findByIco($ico);

            if ($zrsr) {
                if (!$hasDic && !empty($zrsr['dic'])) {
                    $company['dic'] = $zrsr['dic'];
                    $hasDic = true;
                }

                if (!$hasIcdph && !empty($zrsr['ic_dph'])) {
                    $company['ic_dph'] = $zrsr['ic_dph'];
                    $hasIcdph = true;
                }
            }
        } catch (\Throwable $e) {
            Log::channel('icoatlas')->error('zrsr.enrich.error', [
                'ico'   => $ico,
                'error' => $e->getMessage(),
            ]);
        }

        // 2) RÚZ (len ak stále niečo chýba)
        if (!$hasDic || !$hasIcdph) {
            try {
                $ruz = $this->ruz->findByIco($ico);

                if ($ruz) {
                    if (!$hasDic && !empty($ruz['dic'])) {
                        $company['dic'] = $ruz['dic'];
                        $hasDic = true;
                    }

                    if (!$hasIcdph && !empty($ruz['ic_dph'])) {
                        $company['ic_dph'] = $ruz['ic_dph'];
                        $hasIcdph = true;
                    }
                }
            } catch (\Throwable $e) {
                Log::channel('icoatlas')->error('ruz.enrich.error', [
                    'ico'   => $ico,
                    'error' => $e->getMessage(),
                ]);
            }
        }

        return $company;
    }

    /**
     * Vráti prázdnu štruktúru 12 polí pre neznámu firmu.
     *
     * @return array{
     *   ico: string,
     *   name: string|null,
     *   dic: string|null,
     *   ic_dph: string|null,
     *   legal_form: string|null,
     *   address: string|null,
     *   city: string|null,
     *   zip: string|null,
     *   district: string|null,
     *   region: string|null,
     *   country: string|null,
     *   source: string|null,
     * }
     */
    private function emptyCompany(string $ico): array
    {
        return [
            'ico'        => $ico,
            'name'       => null,
            'dic'        => null,
            'ic_dph'     => null,
            'legal_form' => null,
            'address'    => null,
            'city'       => null,
            'zip'        => null,
            'district'   => null,
            'region'     => null,
            'country'    => 'SK',
            'source'     => 'not-found',
        ];
    }

    /**
     * Uistí sa, že sú vždy prítomné všetky kľúče a typy.
     *
     * @param  array<string, mixed> $company
     * @return array{
     *   ico: string,
     *   name: string|null,
     *   dic: string|null,
     *   ic_dph: string|null,
     *   legal_form: string|null,
     *   address: string|null,
     *   city: string|null,
     *   zip: string|null,
     *   district: string|null,
     *   region: string|null,
     *   country: string|null,
     *   source: string|null,
     * }
     */
    private function normalizeCompanyArray(array $company): array
    {
        $defaults = $this->emptyCompany((string) ($company['ico'] ?? ''));

        $merged = array_merge($defaults, $company);

        $merged['ico'] = (string) $merged['ico'];

        return $merged;
    }

    /**
     * Backward compatibility - stará metóda pre testy
     * @deprecated Použi lookupByIco namiesto toho
     */
    public function findByIco(string $ico): array
    {
        $result = $this->lookupByIco($ico);
        return $result['data'];
    }
}
