<?php

namespace App\Jobs;

use App\Models\Arsip;
use Illuminate\Bus\Queueable;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;

class GenerateSummary implements ShouldQueue
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
        try {
            $response = Http::timeout(300)->get("https://cape-republicans-alter-latest.trycloudflare.com/summarize_abstractive/{$this->arsipId}");

            if ($response->successful()) {
                $summary = $response->json('summary_abstractive');
                $arsip = Arsip::find($this->arsipId);
                if ($arsip) {
                    $arsip->update(['summary_abstractive' => $summary]);
                }
            }
        } catch (\Exception $e) {
            Log::error("Gagal membuat ringkasan abstraktif untuk arsip ID {$this->arsipId}: " . $e->getMessage());
        }
    }
}
