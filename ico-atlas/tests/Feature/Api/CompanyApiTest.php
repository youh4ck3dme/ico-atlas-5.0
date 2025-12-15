<?php

namespace Tests\Feature\Api;

use Tests\TestCase;
use Illuminate\Testing\Fluent\AssertableJson;

class CompanyApiTest extends TestCase
{
    public function test_returns_422_for_invalid_ico(): void
    {
        $response = $this->getJson('/api/company/search?ico=123');

        $response->assertStatus(422)
            ->assertJson(fn (AssertableJson $json) =>
                $json->has('message')
                     ->has('errors.ico')
            );
    }

    public function test_returns_422_for_missing_ico(): void
    {
        $response = $this->getJson('/api/company/search');

        $response->assertStatus(422)
            ->assertJson(fn (AssertableJson $json) =>
                $json->has('message')
                     ->has('errors.ico')
            );
    }

    public function test_returns_stable_contract_for_valid_ico(): void
    {
        $response = $this->getJson('/api/company/search?ico=52374220');

        $response->assertStatus(200)
            ->assertJson(fn (AssertableJson $json) =>
                $json->has('data')
                     ->has('meta')
                     ->has('data.ico')
                     ->has('data.name')
                     ->has('data.source')
                     ->has('meta.latency_ms')
                     ->has('meta.cached')
                     ->where('data.country', 'SK')
            );

        // Verify contract structure
        $data = $response->json('data');
        $this->assertArrayHasKey('ico', $data);
        $this->assertArrayHasKey('name', $data);
        $this->assertArrayHasKey('dic', $data);
        $this->assertArrayHasKey('ic_dph', $data);
        $this->assertArrayHasKey('legal_form', $data);
        $this->assertArrayHasKey('address', $data);
        $this->assertArrayHasKey('city', $data);
        $this->assertArrayHasKey('zip', $data);
        $this->assertArrayHasKey('district', $data);
        $this->assertArrayHasKey('region', $data);
        $this->assertArrayHasKey('country', $data);
        $this->assertArrayHasKey('source', $data);
    }

    public function test_returns_json_format_for_valid_ico(): void
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
    }
}

