<?php

namespace App\Services\Company\Providers;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class ZrsrProvider
{
    /**
     * Získa údaje zo Živnostenského registra (ZRSR) podľa IČO.
     *
     * ✋ IMPORTANT:
     *  - Táto verzia je SAFE skeleton – reálne HTTP volanie je voliteľné.
     *  - Môžeš použiť:
     *      • priamy scraping HTML (ak je právne OK),
     *      • alebo open-data proxy / microservice,
     *      • alebo interné DB / cache.
     *
     * @return array{
     *   dic: string|null,
     *   ic_dph: string|null,
     * }|null
     */
    public function findByIco(string $ico): ?array
    {
        // TODO: implement real ZRSR integration.
        // DEMO / SAFE IMPLEMENTATION: vždy null = žiadne dáta.
        // Tým pádom sa nič nepokazí, ale pipeline je pripravená.

        // Príklad budúcej implementácie (pseudo-kód):
        //
        // try {
        //     $response = Http::timeout(10)->get('https://zrsr-api.local/ico/' . $ico);
        //
        //     if (!$response->ok()) {
        //         Log::channel('icoatlas')->warning('ZRSR non-200', [
        //             'ico' => $ico,
        //             'status' => $response->status(),
        //         ]);
        //         return null;
        //     }
        //
        //     $payload = $response->json();
        //
        //     return [
        //         'dic'    => $payload['dic'] ?? null,
        //         'ic_dph' => $payload['ic_dph'] ?? null,
        //     ];
        //
        // } catch (\Throwable $e) {
        //     Log::channel('icoatlas')->error('ZRSR error', [
        //         'ico'   => $ico,
        //         'error' => $e->getMessage(),
        //     ]);
        //     return null;
        // }

        return null;
    }
}

