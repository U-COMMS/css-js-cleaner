import json
import os
import errno

initial_file = "coverage-bing.json"
compare_files = ["coverage-search.json"]
domain_name = "https://www.bing.com"

def clean_range(initial_data, append_data):
  new_range = []
  for i in range(len(initial_data)):
    try:
      if i < len(initial_data):
        last_result = False
      else:
        last_result = True
    except:
      last_result = True

    skip_to = -1
    if i > skip_to:
      if last_result:
        if append_data['start'] >= initial_data[i]['start'] and append_data['end'] <= initial_data[i]['end']:
          # print("sits inside block ##IGNORE")
          new_range.append(initial_data[i])
        elif append_data['start'] >= initial_data[i]['start'] and append_data['start'] <= initial_data[i]['end'] and append_data['end'] > initial_data[i]['end']:
          # print("starts inside last block and ends outside")
          new_payload = { 'start': initial_data[i]['start'], 'end': append_data['end'] } # modify final payload
          new_range.append(new_payload) # append final payload
        elif append_data['start'] >= initial_data[i]['end']:
          # print('starts after last')
          new_range.append(initial_data[i]) # append as append_data starts after block
          new_range.append(append_data) # append as passed last block
      else:
        if append_data['start'] >= initial_data[i]['start'] and append_data['end'] <= initial_data[i]['end']:
          # print("sits inside block ##IGNORE")
          new_range.append(initial_data[i])
        elif append_data['start'] >= initial_data[i]['start'] and append_data['start'] <= initial_data[i]['end'] and append_data['end'] > initial_data[i]['end']:
          # print("starts inside block and ends outside")
          ## CHECK WHERE END AND EXTENDS BLOCK
          if append_data['end'] < initial_data[i+1]['start']:
            # print("  ends before next block")
            new_payload = { 'start': initial_data[i]['start'], 'end': append_data['end'] } # modify payload
            new_range.append(new_payload) # append payload
          elif append_data['end'] > initial_data[i+1]['start'] and append_data['end'] <= initial_data[i+1]['end']:
            # print("  ends inside next block")
            new_payload = { 'start': initial_data[i]['start'], 'end': initial_data[i+1]['end'] } # modify payload
            new_range.append(new_payload) # append payload
          else:
            # print("  ends in later block")
            for x in range(len(initial_data)):
              if append_data['end'] > initial_data[x]['start'] and append_data['end'] > initial_data[x]['end']:
                end_in = x + 1
            new_payload = { 'start': initial_data[i]['start'], 'end': initial_data[end_in]['end'] } # modify payload
            new_range.append(new_payload) # append payload
            skip_to = end_in

        elif append_data['start'] > initial_data[i]['end'] and append_data['end'] < initial_data[i+1]['start']:
          # print("sits between blocks ##ADD BLOCK")
          new_range.append(initial_data[i]) # append as append_data starts after block
          new_range.append(append_data) # append new block after first
        elif append_data['start'] > initial_data[i]['end'] and append_data['start'] < initial_data[i+1]['start']:
          # print("starts between blocks")
          ## CHECK WHERE END AND APPEND
          if append_data['end'] < initial_data[i+1]['start']:
            # print("  ends before next block")
            new_payload = { 'start': append_data['start'], 'end': append_data['end'] } # modify payload
            new_range.append(new_payload) # append payload
          elif append_data['end'] > initial_data[i+1]['start'] and append_data['end'] <= initial_data[i+1]['end']:
            # print("  ends inside next block")
            new_payload = { 'start': append_data['start'], 'end': initial_data[i+1]['end'] } # modify payload
            new_range.append(new_payload) # append payload
          else:
            # print("  ends in later block")
            for x in range(len(initial_data)):
              if append_data['end'] > initial_data[x]['start'] and append_data['end'] > initial_data[x]['end']:
                end_in = x + 1
            new_payload = { 'start': append_data['start'], 'end': initial_data[end_in]['end'] } # modify payload
            new_range.append(new_payload) # append payload
            skip_to = end_in
        elif append_data['start'] >= initial_data[i]['end']:
          # print('starts after')
          new_range.append(initial_data[i]) # append as append_data starts after block
        elif append_data['end'] <= initial_data[i]['start']:
          # print('starts before')
          # CHECK IF APPENDED BLOCK OVERLAPS
          new_range.append(initial_data[i]) # append as append_data starts before block and doesn't overla
  return new_range

with open(initial_file) as json_file:
  data = json.load(json_file)
  if os.path.exists("coverage.json"):
    os.remove("coverage.json")
  with open('coverage.json', 'w') as outfile:
    json.dump(data, outfile)

with open('coverage.json') as json_file:
  coverage_data = json.load(json_file)["data"]
  cleaned_data = coverage_data

  if compare_files:
    for compare_file in compare_files:
      with open(compare_file) as next_json_file:
        next_file_data = json.load(next_json_file)["data"]

      ci = 0
      for coverage_file in cleaned_data:
        cleaning_range = coverage_file['ranges']
        for next_file in next_file_data:
          if next_file["url"] == coverage_file["url"]:
            print("## Cleaning File: %s" % (coverage_file["url"]))
            for home_range in next_file['ranges']:
              cleaning_range = clean_range(cleaning_range, home_range)
        cleaned_data[ci]["ranges"] = cleaning_range

# f = open("temp.json", "a")
# f.write(json.dumps(cleaned_data))
# f.close()

# Clean Files
for file in cleaned_data:
  if domain_name in file["url"] and (".css" in file["url"] or ".js" in file["url"]):
    used_data = ""
    for used_range in file['ranges']:
      substring = file["text"][used_range["start"]:used_range["end"]]
      used_data += substring + "\n"

    filename = "./cleaned/" + file["url"].replace(domain_name, ".")
    if not os.path.exists(os.path.dirname(filename)):
      try:
        os.makedirs(os.path.dirname(filename))
      except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
          raise
    f = open(filename, "a")
    f.write(used_data)
    f.close()
