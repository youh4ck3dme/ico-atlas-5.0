<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\CompanyController;

Route::middleware(['throttle:company-search'])->group(function () {
    Route::get('/company/search', [CompanyController::class, 'search']);
});

