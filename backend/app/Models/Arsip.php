<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Arsip extends Model
{
    use HasFactory;

    protected $fillable = ['judul', 'kategori', 'klasifikasi', 'file_path', 'hasil_ocr'];

    public function bookmarkedBy(){
        return $this->hasMany(Bookmark::class);
    }
}
