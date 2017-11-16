#!/usr/bin/env ruby

require 'json'

old, new = $stdin.read.split("\n")

if not new
    new = old
end

old = JSON.parse old, {:symbolize_names => true}
new = JSON.parse new, {:symbolize_names => true}

if /^Buy$|^Buy\./ =~ new[:project] and not new.key?(:due) and not old.key?(:wait)
    new[:wait] = 'someday'
    puts new.to_json
    puts 'Set due:someday for Buy* project'
else
    puts new.to_json
end

exit 0
