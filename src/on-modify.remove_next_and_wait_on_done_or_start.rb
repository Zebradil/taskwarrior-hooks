#!/usr/bin/env ruby

require 'json'

args = {}

ARGV.each do|arg|
    key, value = arg.split(':', 2)
    args[key.to_sym] = value
end

# Skip first line which contains info about old state
$stdin.readline
new = JSON.parse $stdin.readline, {:symbolize_names => true}

messages = []
if %w/done start/.include? args[:command]
    unless new[:wait].to_s.empty?
        new.delete :wait
        messages << '"wait" field was erased'
    end

    if new[:tags].to_a.include? 'next'
        new[:tags].delete 'next'
        messages << '"next" tag was deleted'
    end
end

puts new.to_json
puts messages * '\n'

exit 0
