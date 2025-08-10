<?php

namespace App\Jobs;

use App\Models\Arsip;
use Illuminate\Bus\Queueable;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Log;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use App\Jobs\GenerateSummary;

class ProcessOCR implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $arsipId;

    /**
     * Create a new job instance.
     */
    public function __construct($arsipId)
    {
        $this->arsipId = $arsipId;
    }

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $arsip = Arsip::find($this->arsipId);
        $fileContent = Storage::get($arsip->file_path);

        $response = Http::attach(
            'file', $fileContent, basename($arsip->file_path)
        )->post('http://localhost:5000/ocr');

        if ($response->successful()) {
            $hasil = $response->json('hasil_ocr') ?? 'Tidak ada teks OCR ditemukan.';
            $arsip->update(['hasil_ocr' => $hasil]);

            GenerateSummary::dispatch($arsip->id);
        } else {
            Log::error("Gagal OCR untuk arsip ID {$arsip->id}: " . $response->body());
        }
    }
}
