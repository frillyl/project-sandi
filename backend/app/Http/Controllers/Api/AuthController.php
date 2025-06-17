<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\ValidationException;
use App\Models\User;

class AuthController extends Controller
{
    public function login(Request $request){
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (!Auth::attempt($credentials)) {
            throw ValidationException::withMessages([
                'email' => ['Email atau Password salah.'],
            ]);
        }

        $user = $request->user();

        $token = $user->createToken('sandi-token')->plainTextToken;

        return response()->json([
            'message' => 'Login Berhasil!',
            'token' => $token,
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
                'role' => $user->role,
                'is_default_password' => $user->is_default_password,
            ]
        ]);
    }

    public function changePassword(Request $request){
        $request->validate([
            'password' => 'required|confirmed|min:8',
        ]);

        $user = $request->user();
        $user->password = bcrypt($request->password);
        $user->is_default_password = false;
        $user->save();

        return response()->json(['message' => 'Password berhasil diubah.']);
    }

    public function logout(Request $request){
        $request->user()->currentAccessToken()->delete();

        return response()->json(['message' => 'Logout Berhasil!']);
    }

    public function user (Request $request){
        $user = Auth::user();

        return response()->json([
            'name' => $user->name,
            'email' => $user->email,
            'role' =>$user->role,
            'is_default_password' => $user->is_default_password
        ]);
    }

    public function forgotPassword(Request $request) {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email|exists:users,email',
        ]);

        if ($validator->fails()) {
            return response()->json(['errors' => $validator->errors()], 422);
        }

        $status = Password::sendResetLink($request->only('email'));

        if ($status === Password::RESET_LINK_SENT) {
            return response()->json(['message' => 'Link reset password telah dikirim ke email Anda.']);
        } else {
            return response()->json(['message' => 'Gagal mengirim link reset password.'], 500);
        }
    }
}
