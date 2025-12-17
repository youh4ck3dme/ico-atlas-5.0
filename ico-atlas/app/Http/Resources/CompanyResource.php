<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class CompanyResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
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
}

