# Lab Assignment #2 - Linux Commands for Digital Forensic Investigation

## 1. Student name and enrolment number

- Name: YOUR NAME
- Enrolment number: YOUR ROLL NUMBER
- Course: MSDF26-PC-103 Programming for Digital Forensics, M.Sc. DFIS Semester I

## 2. Date and time of investigation

30 September 2026, around 05:27 UTC (taken from the `date` command, saved in `logs/investigation_details.txt`).
Machine: hostname `vm`, user `root`, working directory `/home/user/PDF/DF_Lab_Assignment_2`.

## 3. Objective of the investigation

To use basic Linux commands to set up a forensic workspace, create some sample evidence files, and examine them without changing the originals. The work covers file metadata, permissions, searching, log analysis, hashing to prove integrity, keeping a command history, and finally archiving the results.

## 4. Description of the evidence files

All five files are in `evidence/`. I made them myself with `echo` for this lab.

| File | Size | What it contains |
|---|---|---|
| system_log.txt | 944 bytes | 12 lines of fake syslog: successful and failed ssh logins, a disk error, a sudo denial, a cron job, an unauthorized access attempt, an HTTP 500 error |
| login_records.txt | 428 bytes | 10 comma separated login records (user, ip, date, time, status). Some are repeated on purpose |
| user_notes.txt | 223 bytes | Four lines of personal notes, one mentions changing the admin password and one mentions /etc/shadow |
| suspicious_script.sh | 171 bytes | A small bash script with a hard coded password, that dumps /etc/passwd and downloads a file with wget. It was never executed |
| .hidden_note.txt | 86 bytes | Hidden file with a "secret key" and a temporary ftp login |

The originals were never edited after creation. Every analysis step was done on the copies in `working_copy/`.

## 5. Commands used

| Task | Commands |
|---|---|
| 1. Workspace | `pwd`, `mkdir`, `cd` (relative and absolute paths), `ls`, `ls -R > directory_structure.txt` |
| 2. Evidence files | `touch`, `echo >>`, `ls -la`, `cp`, `mv`, `diff` |
| 3. Metadata | `ls -lh`, `file`, `stat` |
| 4. Permissions | `ls -l`, `stat -c`, `chmod u+x`, `chmod go-w` |
| 5. Searching | `find` (with `-name`, `-mtime -1`, `-size +300c`, `-perm -u+x`), `grep -rli` |
| 6. Log analysis | `cat`, `head -5`, `tail -5`, `wc -l -w -m`, `grep`, `grep -i`, `grep -n`, `grep -inE` |
| 7. Sorting | `sort`, `uniq`, `uniq -c`, `uniq -d`, `cut -d, -f`, `sort -t, -k1,1` |
| 8. Hashing | `md5sum`, `sha256sum`, `diff`, `sed` |
| 9. Audit trail | `history`, `whoami`, `date`, `hostname`, `pwd` |
| 10. Archive | `tar -czvf`, `tar -tzvf`, `ls -lh`, `sha256sum` |

The full list of commands is in `logs/command_history.txt` and the terminal output of the whole session is in `terminal_output.txt`.

## 6. File metadata observations

Saved in `logs/file_metadata.txt` (from `ls -lh`, `file` and `stat`).

| File | Type (`file`) | Size | Owner:Group | Perm | Modified (and metadata change) |
|---|---|---|---|---|---|
| system_log.txt | ASCII text | 944 | root:root | 644 | 05:27:04.45 |
| login_records.txt | CSV ASCII text | 428 | root:root | 644 | 05:27:04.96 |
| user_notes.txt | ASCII text | 223 | root:root | 644 | 05:27:05.17 |
| suspicious_script.sh | Bourne-Again shell script, ASCII text executable | 171 | root:root | 644 | 05:27:05.48 |
| .hidden_note.txt | ASCII text | 86 | root:root | 644 | 05:27:05.58 |

Observations:
- Everything is owned by `root:root` with `rw-r--r--` (644), which is the default when a file is created with umask 022.
- `file` identifies suspicious_script.sh as a shell script even though it is not executable yet, because it looks at the content (the `#!/bin/bash` line) and not only the extension.
- For these files the modification time and the metadata change (ctime) time are the same, because the last thing that happened to each of them was the write that created its content. If somebody had run `chmod` on them later, only the ctime would have moved.
- Access time is a little later than modification time (05:27:05.74 onwards) because the files were read by `cp` when the working copies were made. This is the reason the analysis was done on copies, reading an original updates its access time.
- The birth time (`Birth:` in `stat`) is 05:27:03.83 for all five files, because a single `touch` command created them together. The content was added afterwards, which is why the modification times are later.

## 7. Permission analysis

Done only on `working_copy/suspicious_script.sh`.

| | Before | After |
|---|---|---|
| Symbolic | `-rw-r--r--` | `-rwxr--r--` |
| Numeric | 644 | 744 |

- Owner (root): read and write before, now read, write and execute.
- Group (root): read only, no change.
- Others: read only, no change.

Commands used were `chmod u+x suspicious_script.sh` and `chmod go-w suspicious_script.sh`. The second command did not change anything, because group and others did not have write permission to begin with.

Forensic importance of permissions and ownership:
- Ownership tells us which user account created or controls a file, so it can link a file to a person or process.
- Permissions show who was allowed to read, change or run the file. A script that is world writable or has execute permission is more suspicious than a normal text file.
- An unexpected permission, like a file in /tmp with the execute bit set, can point to malware or a backdoor.
- Changing permissions changes the metadata change time (ctime), so doing it on the original would destroy evidence about when the file was last touched. That is why it was done on the working copy only.

## 8. Search results

Full output in `logs/file_search_results.txt`.

- `.txt` files: 4 in `evidence/`, 4 in `working_copy/` (the copy of user_notes.txt is called examined_notes.txt), plus a few log files that I created myself in the workspace.
- `.sh` files: `evidence/suspicious_script.sh` and `working_copy/suspicious_script.sh`.
- Hidden files: `.hidden_note.txt` in both `evidence/` and `working_copy/`.
- Files containing the word "password" (case insensitive): user_notes.txt, system_log.txt and suspicious_script.sh, in both evidence and working_copy.
- Modified in the last 24 hours: all files, since they were all created today.
- Larger than 300 bytes: system_log.txt and login_records.txt (originals and copies), plus my own log files.
- Executable permission: only `working_copy/suspicious_script.sh`, since I added the execute bit in Task 4. The original is still not executable.

## 9. Suspicious log entries

Saved in `extracted/suspicious_entries.txt` (14 lines, from `grep -inE 'failed|error|unauthorized|login|root'`).

Keyword counts (case sensitive `grep`, both files together):

| Keyword | Matches |
|---|---|
| failed | 5 (1 disk error line, 4 login records) |
| error | 1 |
| unauthorized | 2 |
| login | 1 |
| root | 7 |

When the search is made case insensitive, "Failed password for root" (3 lines) and "Unauthorized access attempt" and "ERROR 500" also match. So a plain case sensitive search missed the most important lines.

Main suspicious entries:
- `system_log.txt` lines 2 - 4: three failed ssh password attempts for `root` from 10.0.0.45 within about 20 seconds (looks like a brute force attempt).
- `system_log.txt` line 8: "Unauthorized access attempt from 172.16.5.9".
- `system_log.txt` line 5: kernel error about disk sda2 write failure.
- `system_log.txt` line 12: HTTP 500 error on /admin/upload.php.
- `login_records.txt`: root failed 3 times from 10.0.0.45, guest was unauthorized (recorded twice) from 172.16.5.9, john failed once.

Results of the sorting in Task 7 (`extracted/processed_login_records.txt`): there are 10 records but only 8 unique ones. Two records are repeated, `guest,172.16.5.9,...,10:45,unauthorized` twice and `root,10.0.0.45,...,08:05,failed` twice.

Line, word and character counts: system_log.txt has 12 lines, 137 words, 944 characters. login_records.txt has 10 lines, 10 words, 428 characters.

## 10. Original and working-copy hash values

Original hashes are saved in `logs/original_hashes.txt`.

| File | MD5 (original) | SHA-256 (original) | SHA-256 (working copy) |
|---|---|---|---|
| login_records.txt | 7a1cc8502504de7741d3ba0d2d1dc691 | afd4c67f8210d5e261ab866eaef9b4c0ccc7b86c66266b99db79eec7a579ffbe | same |
| suspicious_script.sh | 84b36fcce240ef32c68dd12afdf5fac6 | 13962807d450a07fb66ed665edbfd0f0596969245c1a8034d1e01dc5ab16d9da | same |
| system_log.txt | bfe5a194c02c08142c2e4d18facf1c5d | 4d3cd1e8c5d6d2ab088bde3d7f92a94a7ad648127d7415b3d144e9cb13d62bca | same |
| user_notes.txt | 3567ffe214e77fb007ccf5d9ccf826dc | aca9f05608ebcac0b8eb863b40412e8d31aa2992ce409d7f7c163a200e962843 | same (examined_notes.txt) |
| .hidden_note.txt | 847e996ed1dd0e636559c2a8e9def95e | c90224049746b32f2593da6f939ae69e39c86ef8248f4354ac5ef237bff1d6e7 | same |

The working copy hashes are in `logs/working_copy_hashes.txt`.

## 11. Integrity verification result

- The SHA-256 of every working copy was compared with the original using `diff`. The only thing I changed before comparing was the name examined_notes.txt back to user_notes.txt with `sed`, because that file was renamed in Task 2. There was no difference, so all copies were exact.
- The `chmod` in Task 4 did not affect the hashes, because a hash only depends on file content and not on permissions or timestamps.
- After that I added one line to `working_copy/system_log.txt` on purpose:

| | SHA-256 |
|---|---|
| evidence/system_log.txt | 4d3cd1e8c5d6d2ab088bde3d7f92a94a7ad648127d7415b3d144e9cb13d62bca |
| working_copy/system_log.txt (modified) | 3410df5c1aad033ec5bc6347ddf8616f2c997d4d431a21e0e02778c4fdeb17a6 |

Why the hash changed: a hash function like SHA-256 processes every byte of the file, so even a single added character gives a completely different value (avalanche effect). It is not possible to change the file and keep the same hash in practice. This is what makes hashes useful to prove that evidence has not been tampered with.

Finally, the original files were checked again against `original_hashes.txt` with `sha256sum -c` and all five gave OK, so the evidence directory was not altered during the investigation.

## 12. Important findings

1. Three failed root logins in a row from 10.0.0.45 in the log and in the login records, which looks like a password guessing attack.
2. The address 172.16.5.9 appears as an unauthorized access attempt in the log, is the `guest` user in the login records (twice), and is also the server that suspicious_script.sh downloads `payload.sh` from. So it is probably linked with the same activity.
3. suspicious_script.sh contains a plain text password (`admin123`), copies /etc/passwd to /tmp and downloads and makes a file executable. It should not be run.
4. `sudo` log shows user john trying to read /etc/shadow and was refused, and user_notes.txt also mentions john copying files from /etc/shadow.
5. The hidden file .hidden_note.txt holds a secret key and an ftp username and password in plain text.
6. The word "password" is stored in three of the five files.
7. Hashes of the copies match the originals, and after modifying one copy the hash changed, which shows that hashing detects changes.

## 13. Conclusion

The forensic workspace was created and the sample evidence was handled the correct way: originals were left alone, analysis was done on working copies, and hashes were taken before and after to prove integrity. Metadata, permission, search, log and sorting commands were enough to find several suspicious things in the sample data (brute force attempts, an unauthorized access, a dangerous script and stored credentials). The command history and the investigation details were saved so that each step can be repeated and checked by someone else, and the logs, extracted data and this report were put into a compressed archive whose SHA-256 was recorded.

Note: the sample data is fictional and was created only for this lab.
