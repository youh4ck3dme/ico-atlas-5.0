<?php

namespace App\Services\Company\Providers;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class RuzProvider
{
    /**
     * Získa údaje z Registra účtovných závierok (RÚZ) podľa IČO.
     *
     * Primárne vhodné na:
     *  - finančné agregáty (obrat, zisk, aktíva...),
     *  - doplňujúci zdroj pre DIC / IČ DPH.
     *
     * @return array{
     *   dic: string|null,
     *   ic_dph: string|null,
     *   // future: revenue, profit, employees, ...
     * }|null
     */
    public function findByIco(string $ico): ?array
    {
        // TODO: implement real RÚZ integration.
        // DEMO / SAFE IMPLEMENTATION: vždy null.

        // Pseudo-kód budúcej implementácie:
        //
        // try {
        //     $response = Http::timeout(10)->get('https://ruz-api.local/ico/' . $ico);
        //
        //     if (!$response->ok()) {
        //         Log::channel('icoatlas')->warning('RÚZ non-200', [
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
        //     Log::channel('icoatlas')->error('RÚZ error', [
        //         'ico'   => $ico,
        //         'error' => $e->getMessage(),
        //     ]);
        //     return null;
        // }

        return null;
    }
}

