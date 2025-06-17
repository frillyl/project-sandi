<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Response;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/arsip/file/{filename}', function ($filename) {
    $path = storage_path('app/private/arsip/' . $filename);

    if (!file_exists($path)) {
        abort(404);
    }

    return response()->file($path);
});

Route::get('password/reset/{token}', function ($token) {
    return redirect()->to("http://localhost:5173/demo/reset-password?token=$token");
})->name('password.reset');

