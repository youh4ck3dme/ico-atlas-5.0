<?php

namespace App\Http\Controllers\Api;

use App\Data\CompanyProfileData;
use App\Http\Controllers\Controller;
use App\Http\Requests\CompanySearchRequest;
use App\Http\Resources\CompanyResource;
use App\Services\CompanyService;
use Illuminate\Http\JsonResponse;

class CompanyController extends Controller
{
    public function __construct(
        protected CompanyService $service,
    ) {}

    /**
     * 🔒 CONTRACT-LOCK ZÓNA
     *
     * JSON štruktúra:
     *  - data: 12 keys (pozri API_CONTRACT_LOCK.md)
     *  - meta: cached, latency_ms
     *
     * VAROVANIE:
     *  - Ak chceš čokoľvek meniť, musíš:
     *      1) upraviť API_CONTRACT_LOCK.md
     *      2) upraviť CompanyContractLockTest
     *      3) bumpnúť verziu API (breaking change)
     */
    public function search(CompanySearchRequest $request): JsonResponse
    {
        $ico = $request->validated('ico');

        try {
            $result = $this->service->lookupByIco($ico);

            // Ak je source 'not-found', vráť 404
            if ($result['data']['source'] === 'not-found') {
                return response()->json([
                    'message' => 'Company not found',
                    'data'    => null,
                    'meta'    => [
                        'cached'     => false,
                        'latency_ms' => $result['meta']['latency_ms'],
                    ],
                ], 404);
            }

            // Použij CompanyResource pre konzistentný formát
            $profile = CompanyProfileData::fromArray($result['data']);
            $resource = (new CompanyResource($profile))
                ->additional([
                    'meta' => [
                        'cached'     => (bool) $result['meta']['cached'],
                        'latency_ms' => (int) $result['meta']['latency_ms'],
                    ],
                ]);

            return $resource->response();
        } catch (\Exception $e) {
            // Log unexpected errors
            \Log::channel('icoatlas')->error('Company search error', [
                'ico'   => $ico,
                'error' => $e->getMessage(),
                'trace' => $e->getTraceAsString(),
            ]);

            return response()->json([
                'message' => 'An error occurred while searching for the company.',
                'data'    => null,
                'meta'    => [
                    'cached'     => false,
                    'latency_ms' => 0,
                ],
            ], 500);
        }
    }
}
