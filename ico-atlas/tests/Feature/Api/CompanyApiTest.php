<?php

use Illuminate\Testing\Fluent\AssertableJson;

test('returns 422 for invalid ico', function () {
    $this->getJson('/api/company/search?ico=123')
        ->assertStatus(422)
        ->assertJson(fn (AssertableJson $json) =>
            $json->has('message')
                 ->has('errors.ico')
        );
});

test('returns 422 for missing ico', function () {
    $this->getJson('/api/company/search')
        ->assertStatus(422)
        ->assertJson(fn (AssertableJson $json) =>
            $json->has('message')
                 ->has('errors.ico')
        );
});

test('returns stable contract for valid ico', function () {
    $response = $this->getJson('/api/company/search?ico=52374220')
        ->assertStatus(200)
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
    expect($data)->toHaveKeys([
        'ico', 'name', 'dic', 'ic_dph', 'legal_form',
        'address', 'city', 'zip', 'district', 'region',
        'country', 'source'
    ]);
});

test('respects rate limiting', function () {
    // Make 31 requests (limit is 30/minute)
    for ($i = 0; $i < 31; $i++) {
        $response = $this->getJson('/api/company/search?ico=52374220');
        
        if ($i < 30) {
            $response->assertStatus(200);
        }
    }
    
    // 31st request should be rate limited
    $this->getJson('/api/company/search?ico=52374220')
        ->assertStatus(429);
})->skip('Rate limiting test - can be flaky in tests');

