<?php

namespace App\Data;

class PostalCodeMap
{
    /**
     * Resolve Slovak ZIP (PSČ) to district & region.
     *
     * @return array{district: string|null, region: string|null}
     */
    public static function resolve(?string $zip): array
    {
        if (!$zip) {
            return ['district' => null, 'region' => null];
        }

        // "811 08" → "81108"
        $normalized = preg_replace('/\s+/', '', $zip);

        // DEMO / CORE SET – kľudne rozšír podľa potreby.
        $map = [
            // ====================================
            // BRATISLAVA – hlavné mesto
            // ====================================
            '81101' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81102' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81103' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81104' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81105' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81106' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81107' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '81108' => ['district' => 'Bratislava I',   'region' => 'Bratislavský kraj'],
            '82101' => ['district' => 'Bratislava II',  'region' => 'Bratislavský kraj'],
            '82102' => ['district' => 'Bratislava II',  'region' => 'Bratislavský kraj'],
            '82103' => ['district' => 'Bratislava II',  'region' => 'Bratislavský kraj'],
            '82104' => ['district' => 'Bratislava II',  'region' => 'Bratislavský kraj'],
            '82105' => ['district' => 'Bratislava II',  'region' => 'Bratislavský kraj'],
            '83101' => ['district' => 'Bratislava III',  'region' => 'Bratislavský kraj'],
            '83102' => ['district' => 'Bratislava III',  'region' => 'Bratislavský kraj'],
            '83103' => ['district' => 'Bratislava III',  'region' => 'Bratislavský kraj'],
            '84101' => ['district' => 'Bratislava IV',   'region' => 'Bratislavský kraj'],
            '84102' => ['district' => 'Bratislava IV',   'region' => 'Bratislavský kraj'],
            '85101' => ['district' => 'Bratislava V',   'region' => 'Bratislavský kraj'],

            // ====================================
            // KOŠICE
            // ====================================
            '04001' => ['district' => 'Košice I',      'region' => 'Košický kraj'],
            '04011' => ['district' => 'Košice I',      'region' => 'Košický kraj'],
            '04013' => ['district' => 'Košice I',      'region' => 'Košický kraj'],

            // ====================================
            // ŽILINA
            // ====================================
            '01001' => ['district' => 'Žilina',        'region' => 'Žilinský kraj'],
            '01007' => ['district' => 'Žilina',        'region' => 'Žilinský kraj'],

            // ====================================
            // NITRA
            // ====================================
            '94901' => ['district' => 'Nitra',         'region' => 'Nitriansky kraj'],
            '94911' => ['district' => 'Nitra',         'region' => 'Nitriansky kraj'],

            // ====================================
            // TRNAVA
            // ====================================
            '91701' => ['district' => 'Trnava',        'region' => 'Trnavský kraj'],
            '91708' => ['district' => 'Trnava',        'region' => 'Trnavský kraj'],

            // ====================================
            // BANSKÁ BYSTRICA
            // ====================================
            '97401' => ['district' => 'Banská Bystrica', 'region' => 'Banskobystrický kraj'],
            '97404' => ['district' => 'Banská Bystrica', 'region' => 'Banskobystrický kraj'],

            // ====================================
            // PREŠOV
            // ====================================
            '08001' => ['district' => 'Prešov',        'region' => 'Prešovský kraj'],
            '08001' => ['district' => 'Prešov',        'region' => 'Prešovský kraj'],

            // ====================================
            // TRENČÍN
            // ====================================
            '91101' => ['district' => 'Trenčín',       'region' => 'Trenčiansky kraj'],
            '91105' => ['district' => 'Trenčín',       'region' => 'Trenčiansky kraj'],
        ];

        $entry = $map[$normalized] ?? null;

        return [
            'district' => $entry['district'] ?? null,
            'region'   => $entry['region'] ?? null,
        ];
    }
}

