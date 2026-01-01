<?php

namespace App\Data;

class CompanyProfileData
{
    public function __construct(
        public readonly string $ico,
        public readonly ?string $name = null,
        public readonly ?string $dic = null,
        public readonly ?string $ic_dph = null,
        public readonly ?string $legal_form = null,
        public readonly ?string $address = null,
        public readonly ?string $city = null,
        public readonly ?string $zip = null,
        public readonly ?string $district = null,
        public readonly ?string $region = null,
        public readonly ?string $country = 'SK',
        public readonly ?string $source = null,
    ) {
    }

    public static function fromArray(array $data): self
    {
        return new self(
            ico: (string) ($data['ico'] ?? ''),
            name: $data['name'] ?? null,
            dic: $data['dic'] ?? null,
            ic_dph: $data['ic_dph'] ?? null,
            legal_form: $data['legal_form'] ?? null,
            address: $data['address'] ?? null,
            city: $data['city'] ?? null,
            zip: $data['zip'] ?? null,
            district: $data['district'] ?? null,
            region: $data['region'] ?? null,
            country: $data['country'] ?? 'SK',
            source: $data['source'] ?? null,
        );
    }

    public function toArray(): array
    {
        return [
            'ico'        => $this->ico,
            'name'       => $this->name,
            'dic'        => $this->dic,
            'ic_dph'     => $this->ic_dph,
            'legal_form' => $this->legal_form,
            'address'    => $this->address,
            'city'       => $this->city,
            'zip'        => $this->zip,
            'district'   => $this->district,
            'region'     => $this->region,
            'country'    => $this->country,
            'source'     => $this->source,
        ];
    }

    public static function stub(string $ico = '52374220'): self
    {
        return new self(
            ico: $ico,
            name: 'DEMO s.r.o.',
            dic: null,
            ic_dph: null,
            legal_form: null,
            address: null,
            city: null,
            zip: null,
            district: null,
            region: null,
            country: 'SK',
            source: 'stub',
        );
    }
}

