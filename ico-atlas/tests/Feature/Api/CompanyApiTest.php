<?php

namespace Tests\Feature\Api;

use Illuminate\Foundation\Testing\RefreshDatabase;
use PHPUnit\Framework\Attributes\Test;
use Tests\TestCase;

class CompanyApiTest extends TestCase
{
    use RefreshDatabase;

    #[Test]
    public function valid_ico_returns_200_with_company_data(): void
    {
        $response = $this->getJson('/api/company/search?ico=52374220');

        $response->assertStatus(200)
            ->assertJsonStructure([
                'data' => [
                    'ico',
                    'name',
                    'dic',
                    'ic_dph',
                    'legal_form',
                    'address',
                    'city',
                    'zip',
                    'district',
                    'region',
                    'country',
                    'source',
                ],
                'meta' => [
                    'cached',
                    'latency_ms',
                ],
            ]);

        $json = $response->json();
        $this->assertSame('52374220', $json['data']['ico']);
        $this->assertSame('SK', $json['data']['country']);
    }

    #[Test]
    public function missing_ico_parameter_returns_422(): void
    {
        $response = $this->getJson('/api/company/search');

        $response->assertStatus(422)
            ->assertJsonStructure([
                'message',
                'errors' => [
                    'ico',
                ],
            ]);
    }

    #[Test]
    public function invalid_ico_format_returns_422(): void
    {
        $response = $this->getJson('/api/company/search?ico=abc123');

        $response->assertStatus(422);
    }

    #[Test]
    public function ico_with_letters_returns_422(): void
    {
        $response = $this->getJson('/api/company/search?ico=1234567a');

        $response->assertStatus(422);
    }

    #[Test]
    public function ico_with_spaces_returns_422(): void
    {
        $response = $this->getJson('/api/company/search?ico=1234 5678');

        $response->assertStatus(422);
    }

    #[Test]
    public function unknown_ico_returns_404(): void
    {
        $response = $this->getJson('/api/company/search?ico=99999999');

        $response->assertStatus(404)
            ->assertJsonStructure([
                'message',
                'data',
                'meta',
            ]);
    }

    #[Test]
    public function response_is_json(): void
    {
        $response = $this->getJson('/api/company/search?ico=52374220');

        $response->assertHeader('Content-Type', 'application/json');
    }

    #[Test]
    public function accepts_valid_8_digit_ico(): void
    {
        $validIcos = ['12345678', '00000000', '99999999'];

        foreach ($validIcos as $ico) {
            $response = $this->getJson("/api/company/search?ico={$ico}");
            $this->assertContains($response->status(), [200, 404], "IČO {$ico} should be accepted");
        }
    }
}
