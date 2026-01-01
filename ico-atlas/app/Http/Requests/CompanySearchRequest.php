<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CompanySearchRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'ico' => ['required', 'string', 'regex:/^\d{8}$/'],
        ];
    }

    public function messages(): array
    {
        return [
            'ico.required' => 'IČO je povinné.',
            'ico.regex' => 'IČO musí mať presne 8 číslic.',
        ];
    }
}

