<?php

namespace App\Services;

use App\Data\PostalCodeMap;

class RegionResolver
{
    /**
     * @return array{district: string|null, region: string|null}
     */
    public function fromZip(?string $zip): array
    {
        return PostalCodeMap::resolve($zip);
    }
}

