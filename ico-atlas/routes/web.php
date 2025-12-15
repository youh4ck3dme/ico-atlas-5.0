<?php

use Illuminate\Support\Facades\Route;

Route::get('/', fn () => view('welcome'))->name('home');
Route::get('/search', fn () => view('search'))->name('search');
Route::get('/dashboard', fn () => view('dashboard'))->name('dashboard');
