<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Models\Bookmark;

class BookmarkController extends Controller
{
    public function index(Request $request){
        $user = $request->user();
        return response()->json(
            $user->bookmarks()->with('arsip')->get()
        );
    }

    public function store(Request $request){
        $validated = $request->validate([
            'arsip_id' => 'required|exists:arsips,id'
        ]);

        $bookmark = Bookmark::firstOrCreate([
            'user_id' => $request->user()->id,
            'arsip_id' => $validated['arsip_id']
        ]);

        return response()->json($bookmark, 201);
    }

    public function destroy(Request $request, $arsip_id){
        $deleted = Bookmark::where('user_id', $request->user()->id)
            ->where('arsip_id', $arsip_id)
            ->delete();

        return response()->json(['message' => 'Bookmark dihapus', 'deleted']);
    }
}
