ardour { ["type"] = "EditorAction", name = "mb:EmbedRegions",
	license     = "MIT",
	author      = "mbirgin",
	description = [[Import previously exported regions]]
}

function factory (params) return function ()
	



	local tmpfile = '/tmp/mb_ardour.tsv'

-- 3. Parse the data to a key-value table (specify a key for each column):
local keyTable = {}
for line in io.lines(tmpfile) do
	local start, pos, len, path1, path2 = line:match("(%d-)\t(%d-)\t(%d*)\t(.-)\t(.*)")
	print(start, pos, len, path1, path2)
	keyTable[#keyTable + 1] = {["start"] = start, ["pos"] = pos, ["len"] = len, ["path1"] = path1, ["path2"] = path2}
end

print(keyTable)

local sel = Editor:get_selection()
for route in sel.tracks:routelist():iter() do
	gtrack = route:to_track()
end


	for idx, t in pairs(keyTable) do
		local files = C.StringVector()

		print(t.pos, t.start, t.len, t.path1, t.path2)
		
		files:push_back(t.path1)
		len2 = string.len (t.path2)		
		if len2>3 then files:push_back(t.path2) end

		gpos = Temporal.timepos_t (t.pos)
		ret = Editor:do_embed (files, Editing.ImportMergeFiles, Editing.ImportToTrack, gpos, ARDOUR.PluginInfo(), gtrack)
		-- ret = Editor:do_embed (files, Editing.ImportMergeFiles, Editing.ImportToTrack, t.pos, ARDOUR.PluginInfo())
ret_files = ret[1]
ret_pos_end = ret[4]


for it3 in ret_files:iter() do
 print("---", it3)
end
-- print(next(ret))
for key, value in pairs(ret) do
  print(key, value)
end

--print("***", ret[5])

-- Get the list of selected tracks
local sel = Editor:get_selection()
for route in sel.tracks:routelist():iter() do
pl = route:to_track():playlist()
print(pl:name())
-- rg = pl:find_next_region(ret_pos_end, ARDOUR.RegionPoint.End, 0)
-- rg = pl:top_region_at(ret_pos_end-1)
print(ret_pos_end:samples())
rg = pl:top_region_at(Temporal.timepos_t(ret_pos_end:samples() - 1))
print("----", rg:name(), rg:length())
print("tbl", t.start, t.len, t.pos)
rg:set_position(Temporal.timepos_t(0), Temporal.timepos_t(0))
--rg:set_start(4410000)
--rg:set_length(t.len, 0)
-- rg:trim_to(t.start, t.len, 0)
rg:trim_to(Temporal.timepos_t (t.start), Temporal.timecnt_t (t.len))
rg:set_position(Temporal.timepos_t(t.pos), Temporal.timepos_t(0))
--rg:cut_front(4410000, 0)
--rg:cut_end(8820000, 0)
--rg:move_start(4467000, 0)
--rg:set_initial_position(660000)

end

	end
	
	-- files:push_back("/home/m1/sil/music/141018-133622.WAV")
	
	-- Editing.ImportAsRegion
	-- Editing.ImportToTrack
	-- Editing.ImportAsTrack
	
	-- local pos = Session:transport_sample ()
	-- Editor:do_import (files,
	-- 	Editing.ImportDistinctFiles, Editing.ImportToTrack, ARDOUR.SrcQuality.SrcBest,
	-- 	ARDOUR.MidiTrackNameSource.SMFTrackName, ARDOUR.MidiTempoMapDisposition.SMFTempoIgnore,
	-- 	pos, ARDOUR.PluginInfo())



end end
