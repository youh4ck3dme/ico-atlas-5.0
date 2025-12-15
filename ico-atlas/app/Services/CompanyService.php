<?php

namespace App\Services;

use Illuminate\Support\Facades\Cache;

class CompanyService
{
    public function findByIco(string $ico): array
    {
        $cacheKey = "company:ico:$ico";
        $ttl = now()->addHour();

        return Cache::remember($cacheKey, $ttl, function () use ($ico) {
            // TODO: napojiť ORSR/ZRSR/RÚZ providery
            return [
                'ico' => $ico,
                'name' => 'DEMO s.r.o.',
                'dic' => null,
                'ic_dph' => null,
                'legal_form' => null,
                'address' => null,
                'city' => null,
                'zip' => null,
                'district' => null,
                'region' => null,
                'country' => 'SK',
                'source' => 'stub',
            ];
        });
    }
}

