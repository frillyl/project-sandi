<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\KlasifikasiController;
use App\Http\Controllers\Api\ArsipController;
use App\Http\Controllers\Api\BookmarkController;
use App\Http\Controllers\Api\ResetPasswordController;

Route::post('/login', [AuthController::class, 'login']);
Route::middleware('auth:sanctum')->post('/logout', [AuthController::class, 'logout']);
Route::middleware('auth:sanctum')->get('/user', [AuthController::class, 'user']);
Route::middleware('auth:sanctum')->post('/change-password', [AuthController::class, 'changePassword']);
Route::post('/forgot-password', [AuthController::class, 'forgotPassword']);
Route::post('/reset-password', [ResetPasswordController::class, 'reset']);
Route::post('/users/{id}/reset-password', [UserController::class, 'resetPassword']);
Route::apiResource('users', UserController::class);
Route::apiResource('klasifikasi', KlasifikasiController::class);
Route::get('/arsip/download/{id}', [ArsipController::class, 'download']);
Route::get('/arsip/statistik', [ArsipController::class, 'statistik']);
Route::apiResource('arsip', ArsipController::class);
Route::middleware('auth:sanctum')->group(function() {
    Route::get('/bookmarks', [BookmarkController::class, 'index']);
    Route::post('/bookmarks', [BookmarkController::class, 'store']);
    Route::delete('/bookmarks/{arsip_id}', [BookmarkController::class, 'destroy']);
});
