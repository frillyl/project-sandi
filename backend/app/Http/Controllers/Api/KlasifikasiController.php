<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Klasifikasi;
use Illuminate\Http\Request;

class KlasifikasiController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(Klasifikasi::all());
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $request->validate([
            'kode' => 'required|unique:klasifikasis',
            'klasifikasi' => 'required',
        ]);

        $klasifikasi = Klasifikasi::create($request->all());
        return response()->json($klasifikasi, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        return response()->json(Klasifikasi::findOrFail($id));
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        $klasifikasi = Klasifikasi::findOrFail($id);

        $request->validate([
            'kode' => 'required|unique:klasifikasis,kode,' . $id,
            'klasifikasi' => 'required',
        ]);

        $klasifikasi->update($request->all());
        return response()->json($klasifikasi);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        $klasifikasi = Klasifikasi::findOrFail($id);
        $klasifikasi->delete();

        return response()->json(null, 204);
    }
}
