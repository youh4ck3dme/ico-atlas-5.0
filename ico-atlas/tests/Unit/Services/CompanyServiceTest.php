<?php

namespace Tests\Unit\Services;

use App\Services\CompanyService;
use App\Services\Company\Providers\OrsrProvider;
use App\Services\Company\Providers\ZrsrProvider;
use App\Services\Company\Providers\RuzProvider;
use App\Services\RegionResolver;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Config;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

class CompanyServiceTest extends TestCase
{
    protected function setUp(): void
    {
        parent::setUp();
        Cache::flush();
    }

    #[Test]
    public function uses_stub_in_testing_environment(): void
    {
        // Nastavíme stub mode
        Config::set('icoatlas.orsr.stub_mode', true);
        
        // V testing env používame skutočný OrsrProvider so stub mode
        $orsr = new OrsrProvider();
        $zrsr = $this->createMock(ZrsrProvider::class);
        $ruz = $this->createMock(RuzProvider::class);
        $regionResolver = $this->createMock(RegionResolver::class);
        
        // RegionResolver pre PSČ mapping
        $regionResolver->method('fromZip')
            ->with('82101')
            ->willReturn([
                'district' => 'Bratislava II',
                'region'   => 'Bratislavský kraj',
            ]);

        $service = new CompanyService($orsr, $zrsr, $ruz, $regionResolver);

        $result = $service->lookupByIco('52374220');

        $this->assertArrayHasKey('data', $result);
        $this->assertArrayHasKey('meta', $result);
        $this->assertSame('52374220', $result['data']['ico']);
        $this->assertSame('orsr', $result['data']['source']);
        $this->assertSame('DEMO s. r. o.', $result['data']['name']);
    }

    #[Test]
    public function returns_cached_flag_on_second_call(): void
    {
        $orsr = $this->createMock(OrsrProvider::class);
        $zrsr = $this->createMock(ZrsrProvider::class);
        $ruz = $this->createMock(RuzProvider::class);
        $regionResolver = $this->createMock(RegionResolver::class);

        $orsr->method('getDetailByIco')->willReturn([
            'ico'        => '52374220',
            'name'       => 'Test Company',
            'dic'        => null,
            'ic_dph'     => null,
            'legal_form' => null,
            'street'     => 'Main St',
            'city'       => 'City',
            'zip'        => '12345',
            'district'   => null,
            'region'     => null,
            'country'    => 'SK',
        ]);

        $regionResolver->method('fromZip')->willReturn([
            'district' => null,
            'region'   => null,
        ]);

        $service = new CompanyService($orsr, $zrsr, $ruz, $regionResolver);

        $first  = $service->lookupByIco('52374220');
        $second = $service->lookupByIco('52374220');

        $this->assertFalse($first['meta']['cached'], 'First call should not be cached');
        $this->assertTrue($second['meta']['cached'], 'Second call should be cached');
    }

    #[Test]
    public function returns_not_found_when_all_providers_fail(): void
    {
        $orsr = $this->createMock(OrsrProvider::class);
        $zrsr = $this->createMock(ZrsrProvider::class);
        $ruz = $this->createMock(RuzProvider::class);
        $regionResolver = $this->createMock(RegionResolver::class);

        $orsr->method('getDetailByIco')->willReturn(null);
        $zrsr->method('findByIco')->willReturn(null);
        $ruz->method('findByIco')->willReturn(null);
        $regionResolver->method('fromZip')->willReturn([
            'district' => null,
            'region'   => null,
        ]);

        $service = new CompanyService($orsr, $zrsr, $ruz, $regionResolver);

        $result = $service->lookupByIco('99999999');

        $this->assertNotNull($result);
        $this->assertArrayHasKey('data', $result);
        $this->assertSame('99999999', $result['data']['ico']);
        $this->assertSame('not-found', $result['data']['source']);
        $this->assertNull($result['data']['name']);
    }

    #[Test]
    public function calculates_latency_correctly(): void
    {
        // Nastavíme stub mode
        Config::set('icoatlas.orsr.stub_mode', true);
        
        // Použijeme skutočný OrsrProvider so stub mode
        $orsr = new OrsrProvider();
        $zrsr = $this->createMock(ZrsrProvider::class);
        $ruz = $this->createMock(RuzProvider::class);
        $regionResolver = $this->createMock(RegionResolver::class);
        
        $regionResolver->method('fromZip')
            ->with('82101')
            ->willReturn([
                'district' => 'Bratislava II',
                'region'   => 'Bratislavský kraj',
            ]);

        $service = new CompanyService($orsr, $zrsr, $ruz, $regionResolver);

        $result = $service->lookupByIco('52374220');

        $this->assertArrayHasKey('meta', $result);
        $this->assertIsInt($result['meta']['latency_ms']);
        $this->assertGreaterThanOrEqual(0, $result['meta']['latency_ms']);
    }
}

