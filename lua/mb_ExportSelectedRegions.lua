ardour { ["type"] = "EditorAction", name = "mb:ExportSelectedRegions",
	license     = "MIT",
	author      = "mbirgin",
	description = [[Export selected regions to be able to import in another session]]
}

function factory (params) return function ()
	-- there is currently no direct way to find the track
	-- corresponding to a [selected] region
	function find_track_for_region (region_id)
		for route in Session:get_tracks():iter() do
			local track = route:to_track();
			local pl = track:playlist ()
			if not pl:region_by_id (region_id):isnil () then
				return track
			end
		end
		assert (0); -- can't happen, region must be in a playlist
	end

	-- get selection
	-- http://manual.ardour.org/lua-scripting/class_reference/#ArdourUI:Selection
	local sel = Editor:get_selection ()

	-- prepare undo operation
	Session:begin_reversible_command ("Export Selected Regions")
	local add_undo = false -- keep track if something has changed

	local proc = ARDOUR.LuaAPI.nil_proc () -- bounce w/o processing -- mb

		tmpfile="/tmp/mb_ardour.tsv"
		file = io.open(tmpfile, "w")
	-- Iterate over Regions part of the selection
	-- http://manual.ardour.org/lua-scripting/class_reference/#ArdourUI:RegionSelection
	for r in sel.regions:regionlist ():iter () do

		local track = find_track_for_region (r:to_stateful():id())
		local playlist = track:playlist ()

		local path1 = r:source(0):to_filesource ():path ()
		local path2 = ""
		if r:master_sources():size() > 1 then path2 = r:source(1):to_filesource():path() end

file:write(r:start():samples (), "\t", r:position ():samples (), "\t", r:length ():samples (), "\t", path1, "\t", path2, "\n")
		--file:write(r:start(), "\t", r:position (), "\t", r:length (), "\t", path1, "\t", path2, "\n")

		-- print(r:position(), r:length())
		print ("Region:", r:name (), r:position (), r:start())
		print( r:isnil(), r:to_stateful ():id (), r:source(0):ancestor_name ())
		print( r:source(0):to_filesource ():path(), r:whole_file () )

	end
	file:close()

-- set to clipboard
-- os.execute("echo say something | xclip -selection clipboard")


end end
