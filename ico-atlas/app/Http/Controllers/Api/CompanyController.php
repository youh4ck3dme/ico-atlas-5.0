<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\CompanySearchRequest;
use App\Services\CompanyService;
use Illuminate\Support\Facades\Cache;

class CompanyController extends Controller
{
    public function __construct(private readonly CompanyService $service)
    {
    }

    public function search(CompanySearchRequest $request)
    {
        $t0 = hrtime(true);
        $ico = $request->validated()['ico'];

        // Check cache hit before service call
        $cacheKey = "company:ico:$ico";
        $cached = Cache::has($cacheKey);

        $data = $this->service->findByIco($ico);

        $latencyMs = (int) ((hrtime(true) - $t0) / 1_000_000);

        return response()->json([
            'data' => [
                'ico' => $data['ico'] ?? $ico,
                'name' => $data['name'] ?? null,
                'dic' => $data['dic'] ?? null,
                'ic_dph' => $data['ic_dph'] ?? null,
                'legal_form' => $data['legal_form'] ?? null,
                'address' => $data['address'] ?? null,
                'city' => $data['city'] ?? null,
                'zip' => $data['zip'] ?? null,
                'district' => $data['district'] ?? null,
                'region' => $data['region'] ?? null,
                'country' => $data['country'] ?? 'SK',
                'source' => $data['source'] ?? 'unknown',
            ],
            'meta' => [
                'cached' => $cached,
                'latency_ms' => $latencyMs,
            ],
        ]);
    }
}

