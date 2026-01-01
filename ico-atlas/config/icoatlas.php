<?php

return [

    // Koľko hodín cache-ujeme výsledky lookupu
    'cache_ttl_hours' => env('ICOATLAS_CACHE_TTL_HOURS', 12),

    // HTTP timeout pre všetky externé zdroje (ORSR, ZRSR, RÚZ)
    'http_timeout' => env('ICOATLAS_HTTP_TIMEOUT', 10),

    'orsr' => [
        // STARÝ HTML portál – search podľa IČO
        'base_url'   => env('ICOATLAS_ORSR_BASE_URL', 'https://www.orsr.sk'),
        'search_url' => env('ICOATLAS_ORSR_SEARCH_URL', 'https://www.orsr.sk/hladaj_ico.asp'),

        // STUB režim – ak true, používa OrsrProvider::stubCompany()
        'stub_mode'  => env('ICOATLAS_ORSR_STUB', true),
    ],

    'zrsr' => [
        // Tu si neskôr doplníš vlastnú proxy / microservice / open-data endpoint
        'base_url'  => env('ICOATLAS_ZRSR_BASE_URL', null),
        'stub_mode' => env('ICOATLAS_ZRSR_STUB', true),
    ],

    'ruz' => [
        // RÚZ endpoint / proxy (keď bude)
        'base_url'  => env('ICOATLAS_RUZ_BASE_URL', null),
        'stub_mode' => env('ICOATLAS_RUZ_STUB', true),
    ],

];

