<?php

namespace Tests\Unit;

use App\Services\RegionResolver;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

class RegionResolverTest extends TestCase
{
    private RegionResolver $resolver;

    protected function setUp(): void
    {
        parent::setUp();
        $this->resolver = new RegionResolver();
    }

    #[Test]
    public function returns_nulls_for_empty_zip(): void
    {
        $result = $this->resolver->fromZip(null);

        $this->assertSame([
            'district' => null,
            'region'   => null,
        ], $result);
    }

    #[Test]
    public function resolves_known_bratislava_zip(): void
    {
        $result = $this->resolver->fromZip('81108');

        $this->assertSame('Bratislava I', $result['district']);
        $this->assertSame('Bratislavský kraj', $result['region']);
    }

    #[Test]
    public function resolves_zip_with_spaces(): void
    {
        $result = $this->resolver->fromZip('811 08');

        $this->assertSame('Bratislava I', $result['district']);
        $this->assertSame('Bratislavský kraj', $result['region']);
    }

    #[Test]
    public function returns_nulls_for_unknown_zip(): void
    {
        $result = $this->resolver->fromZip('99999');

        $this->assertNull($result['district']);
        $this->assertNull($result['region']);
    }
}

