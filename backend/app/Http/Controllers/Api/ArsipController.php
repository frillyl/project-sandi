<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Arsip;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\DB;

class ArsipController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(Arsip::latest()->get());
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $request->validate([
            'judul' => 'required|string|max:255',
            'kategori' => 'required|string|max:255',
            'klasifikasi' => 'required|string|max:255',
            'file' => 'required|file|mimes:pdf|max:5120',
        ]);

        $file = $request->file('file');
        $path = $file->storeAs('arsip', time().'_'.$file->getClientOriginalName());

        $response = Http::attach(
            'file', file_get_contents($file), $file->getClientOriginalName()
        )->post('http://localhost:5000/ocr'); // URL FastAPI

        if ($response->failed()) {
            return response()->json(['error' => 'OCR processing failed', 'details' => $response->body()], 500);
        }

        $hasil_ocr = $response->successful() && $response->json('hasil_ocr')
                ? $response->json('hasil_ocr')
                : 'Tidak ada teks OCR yang ditemukan.';

        $arsip = Arsip::create([
            'judul' => $request->judul,
            'kategori' => $request->kategori,
            'klasifikasi' => $request->klasifikasi,
            'file_path' => $path,
            'hasil_ocr' => $hasil_ocr,
        ]);

        return response()->json($arsip, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Arsip $arsip)
    {
        return $arsip;
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Arsip $arsip)
    {
        $request->validate([
            'judul' => 'sometimes|required|string|max:255',
            'kategori' => 'sometimes|required|string|max:255',
            'klasifikasi' => 'sometimes|required|string|max:255',
            'file' => 'sometimes|file|mimes:pdf|max:5120',
        ]);

        $arsip->update($request->only('judul', 'kategori', 'klasifikasi'));

        if ($request->hasFile('file')) {
        // Hapus file lama dari storage
        Storage::delete($arsip->file_path);

        // Simpan file baru
        $file = $request->file('file');
        $path = $file->storeAs('arsip', time().'_'.$file->getClientOriginalName());

        // Lakukan OCR pada file baru
        $response = Http::attach(
            'file', file_get_contents($file), $file->getClientOriginalName()
        )->post('http://localhost:5000/ocr'); // URL FastAPI

        if ($response->failed()) {
            return response()->json(['error' => 'OCR processing failed', 'details' => $response->body()], 500);
        }

        $hasil_ocr = $response->successful() && $response->json('hasil_ocr')
                    ? $response->json('hasil_ocr')
                    : 'Tidak ada teks OCR yang ditemukan.';

        // Update file_path dan hasil OCR
        $arsip->update([
            'file_path' => $path,
            'hasil_ocr' => $hasil_ocr,
        ]);
    }

        return response()->json($arsip);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Arsip $arsip)
    {
        Storage::delete($arsip->file_path);
        $arsip->delete();

        return response()->json(['message' => 'Arsip deleted.']);
    }

    public function download($id)
    {
        $arsip = Arsip::findOrFail($id);
        $filePath = $arsip->file_path;

        if (!Storage::exists($filePath)) {
            return response()->json(['error' => 'File not found'], 404);
        }

        return Storage::download($filePath, $arsip->judul . '.pdf', [
            'Content-Type' => 'application/pdf',
            'Access-Control-Allow-Origin' => '*',
            'Access-Control-Expose-Headers' => 'Content-Disposition',
        ]);
    }

    public function statistik() {
        $total = Arsip::count();

        $kategori = Arsip::select('kategori', DB::raw('count(*) as jumlah'))
            ->groupBy('kategori')
            ->pluck('jumlah', 'kategori');

        $bulanan = Arsip::selectRaw("DATE_FORMAT(created_at, '%b %Y') as bulan, COUNT(*) as jumlah")
            ->groupBy('bulan')
            ->orderByRaw("MIN(created_at)")
            ->pluck('jumlah', 'bulan');

        return response()->json([
            'total' => $total,
            'kategori' => $kategori,
            'bulanan' => $bulanan,
        ]);
    }
}
