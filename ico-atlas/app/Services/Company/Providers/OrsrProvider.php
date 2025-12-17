<?php

namespace App\Services\Company\Providers;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class OrsrProvider
{
    /**
     * Hlavný vstup – získa detail o firme podľa IČO.
     *
     * Vráti normalized array, ktorý potom CompanyService mapuje na 12-field kontrakt.
     *
     * @return array{
     *   ico: string,
     *   name: string|null,
     *   dic: string|null,
     *   ic_dph: string|null,
     *   legal_form: string|null,
     *   street: string|null,
     *   city: string|null,
     *   zip: string|null,
     *   district: string|null,
     *   region: string|null,
     *   country: string|null,
     * }|null
     */
    public function getDetailByIco(string $ico): ?array
    {
        $ico = $this->normalizeIco($ico);

        if ($ico === null) {
            return null;
        }

        // Ak je v .env zapnutý STUB režim, používame fake data
        if (config('icoatlas.orsr.stub_mode', true)) {
            return $this->stubCompany($ico);
        }

        try {
            $searchUrl = rtrim(config('icoatlas.orsr.search_url'), '/');
            $baseUrl   = rtrim(config('icoatlas.orsr.base_url'), '/');

            // 1) Vyhľadávanie podľa IČO – HTML stránka s výsledkami
            $searchResponse = Http::timeout(config('icoatlas.http_timeout', 10))
                ->get($searchUrl, [
                    'ICO' => $ico,
                ]);

            if (!$searchResponse->ok()) {
                Log::channel('icoatlas')->warning('orsr.search.non_200', [
                    'ico'    => $ico,
                    'status' => $searchResponse->status(),
                ]);
                return null;
            }

            $searchHtml = $searchResponse->body();

            // 2) Z výsledkov vyhľadávania vyberieme prvý odkaz na detail (vypis.asp?ID=...)
            $detailPath = $this->extractDetailPath($searchHtml);

            if (!$detailPath) {
                Log::channel('icoatlas')->info('orsr.search.no_results', [
                    'ico' => $ico,
                ]);
                return null;
            }

            $detailUrl = $baseUrl . '/' . ltrim($detailPath, '/');

            // 3) Načítame detail firmy (výpis)
            $detailResponse = Http::timeout(config('icoatlas.http_timeout', 10))
                ->get($detailUrl);

            if (!$detailResponse->ok()) {
                Log::channel('icoatlas')->warning('orsr.detail.non_200', [
                    'ico'    => $ico,
                    'url'    => $detailUrl,
                    'status' => $detailResponse->status(),
                ]);
                return null;
            }

            $detailHtml = $detailResponse->body();

            // 4) Parse HTML → name, legal_form, address, city, zip
            $parsed = $this->parseDetailHtml($detailHtml);

            if (!$parsed) {
                Log::channel('icoatlas')->warning('orsr.detail.parse_failed', [
                    'ico' => $ico,
                ]);
                return null;
            }

            return [
                'ico'        => $ico,
                'name'       => $parsed['name']       ?? null,
                'dic'        => $parsed['dic']        ?? null,
                'ic_dph'     => $parsed['ic_dph']     ?? null,
                'legal_form' => $parsed['legal_form'] ?? null,
                'street'     => $parsed['street']     ?? null,
                'city'       => $parsed['city']       ?? null,
                'zip'        => $parsed['zip']        ?? null,
                'district'   => $parsed['district']   ?? null,
                'region'     => $parsed['region']     ?? null,
                'country'    => 'SK',
            ];
        } catch (\Throwable $e) {
            Log::channel('icoatlas')->error('orsr.detail.error', [
                'ico'   => $ico,
                'error' => $e->getMessage(),
            ]);

            return null;
        }
    }

    /**
     * Normalizuje IČO – vyhodí nečíselné znaky, kontrola dĺžky.
     */
    private function normalizeIco(string $ico): ?string
    {
        $digits = preg_replace('/\D+/', '', $ico ?? '');

        if (!$digits || strlen($digits) !== 8) {
            return null;
        }

        return $digits;
    }

    /**
     * Extrahuje path na detail z výsledkov vyhľadávania.
     *
     * Typický pattern: <a href="vypis.asp?ID=383465&P=0&SID=2">...
     */
    private function extractDetailPath(string $html): ?string
    {
        // Jednoduché regex riešenie – stačí prvý match na vypis.asp
        if (preg_match('/href="(vypis\.asp\?ID=[^"]+)"/i', $html, $m)) {
            return html_entity_decode($m[1]);
        }

        return null;
    }

    /**
     * Parsovanie detailu – best-effort verzia.
     *
     * HTML ORSR vo výpise obsahuje blok typu:
     *  Obchodné meno: XXX ; Sídlo: Ulica 1. Mesto 123 45 ; IČO: 12 345 678 ; ...
     *
     * Toto je skeleton – v praxi si ho vieš upraviť podľa reálneho HTML.
     *
     * @return array<string, string|null>|null
     */
    private function parseDetailHtml(string $html): ?array
    {
        // Zjednodušíme whitespace
        $text = strip_tags($html);
        $text = preg_replace('/\s+/', ' ', $text);
        $text = trim($text);

        // Obchodné meno
        $name = null;
        if (preg_match('/Obchodné meno:\s*(.+?)\s*;/', $text, $m)) {
            $name = trim($m[1]);
        }

        // Sídlo (celé ako jeden string)
        $rawAddress = null;
        if (preg_match('/Sídlo:\s*(.+?)\s*;/', $text, $m)) {
            $rawAddress = trim($m[1]);
        }

        // IČO (overíme, že matchuje)
        $ico = null;
        if (preg_match('/IČO:\s*([\d\s]{8,})\s*;/', $text, $m)) {
            $ico = preg_replace('/\D+/', '', $m[1]);
        }

        if (!$name && !$rawAddress && !$ico) {
            return null;
        }

        // Rozbitie adresy na street, city, zip
        $street = null;
        $city   = null;
        $zip    = null;

        if ($rawAddress) {
            // Príklad: "Levická 3. Nitra 949 01"
            // 1) nájdeme PSČ (3+2 číslice)
            if (preg_match('/(\d{3}\s?\d{2})/', $rawAddress, $mZip)) {
                $zip = str_replace(' ', '', $mZip[1]);

                // rozdelíme text pred PSČ
                $beforeZip = trim(substr($rawAddress, 0, strpos($rawAddress, $mZip[0])));

                // skúsiť posledné slovo ako city
                $parts = preg_split('/\s+/', $beforeZip);
                if (count($parts) >= 2) {
                    $city   = array_pop($parts);
                    $street = trim(implode(' ', $parts));
                } else {
                    $city   = $beforeZip;
                    $street = null;
                }
            } else {
                // fallback: bez PSČ – celé ako street
                $street = $rawAddress;
            }
        }

        // Legal form – typicky v obchodnom mene (napr. "GLASORA a.s.")
        $legalForm = null;
        if ($name) {
            if (preg_match('/\b(a\.s\.|s\. r\. o\.|spol\. s r\. o\.|v\. o\. s\.|k\. s\.)\b/iu', $name, $mLf)) {
                $legalForm = trim($mLf[1]);
            }
        }

        return [
            'name'       => $name,
            'dic'        => null, // ORSR väčšinou nedáva DIC/DPH – riešime cez ZRSR/RÚZ
            'ic_dph'     => null,
            'legal_form' => $legalForm,
            'street'     => $street,
            'city'       => $city,
            'zip'        => $zip,
            'district'   => null,
            'region'     => null,
        ];
    }

    /**
     * STUB režim – testovacie dáta bez HTTP.
     *
     * Vhodné pre lokálny vývoj, CI testy a offline dev.
     */
    private function stubCompany(string $ico): ?array
    {
        // Jedno demo IČO – plné dáta
        if ($ico === '52374220') {
            return [
                'ico'        => $ico,
                'name'       => 'DEMO s. r. o.',
                'dic'        => null,
                'ic_dph'     => null,
                'legal_form' => 's. r. o.',
                'street'     => 'Drieňová 1J',
                'city'       => 'Bratislava',
                'zip'        => '82101',
                'district'   => null,
                'region'     => null,
                'country'    => 'SK',
            ];
        }

        // Všetko ostatné: zatiaľ null → CompanyService to vyrieši ako not-found
        return null;
    }
}

