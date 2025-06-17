<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use App\Models\Arsip;

class Bookmark extends Model
{
    protected $fillable = ['user_id', 'arsip_id'];

    public function user(){
        return $this->belongsTo(User::class);
    }

    public function arsip(){
        return $this->belongsTo(Arsip::class);
    }
}
