# Disclaimer

**Every page and file published by this project is generated with machine
assistance from official public records. None of it has been reviewed by an
attorney. It is not warranted for any use.**

That sentence is not boilerplate added to satisfy a license. It is the accurate
description of how this material is produced, and readers, redistributors and
anyone quoting this work are asked to carry it forward.

## What this project is

An automated pipeline that takes a public meeting recording, produces a machine
transcript, attributes the transcript to named speakers, and renders a page
summarizing what happened, with timestamps linking back to the moment in the
official recording and with citations to the statutes a proceeding appears to
implicate.

## What this project is not

**It is not legal advice.** Nothing here creates an attorney-client
relationship, and no part of it should be relied on in deciding whether to file
a Right-to-Know complaint, a lawsuit, or any other action. Consult a New
Hampshire attorney.

**It is not a finding.** The pages carry "concern flags" citing statutes such as
RSA 91-A. A flag means that a machine reading of the record raised a question a
human should look at. It does not mean a violation occurred, has been alleged by
anyone, or has been adjudicated. Severity labels on those flags track how
squarely the cited statute fits the facts on the record, not how serious the
underlying conduct is.

**It is not the official record.** The official record of any meeting is the
minutes as approved by the body, and the recording as published by Claremont
Community Television. Where this project disagrees with the minutes, the minutes
control as the legal record and the disagreement itself is what the page is
reporting.

## Known and specific limitations

1. **Automatic speech recognition makes errors, including in names, dollar
   figures and statute numbers.** The project maintains glossaries of recurring
   mistranscriptions, and quoted passages are machine-checked against the
   transcript corpus, but errors survive. A figure or a citation that matters
   should be checked against the recording at the linked timestamp.

2. **Speaker attribution is inferred, and this is the project's most
   consequential failure mode.** Diarized voices are matched to named people
   using rosters, agendas, minutes and self-identification in the recording.
   Attribution is a judgment, not a measurement. It is weakest for members of
   the public: of the 176 named citizens'-comment speakers in this corpus, 121
   appear in exactly one meeting, which means there is no second recording to
   corroborate the voice against and often no document naming them at all.
   Attributing a remark to the wrong resident is not a cosmetic error. It is the
   one thing this pipeline can do that puts words in a private person's mouth.

3. **Summaries are machine-written.** They compress hours of proceedings into
   paragraphs, and compression discards context. Read the linked timestamp
   before relying on a characterization.

4. **Statutory citations may be misapplied.** Citations are verified to exist and
   to say what is quoted. Whether the statute actually governs the facts of a
   given meeting is a legal question the pipeline is not competent to answer.

5. **Coverage is incomplete.** Some meetings have no recording, no packet, no
   minutes, or none of the three. The absence of a page for a meeting means only
   that the project has not processed it.

## Members of the public who speak at meetings

**They are named here, in full.** People who give public comment state their name
and ward into the microphone as a matter of course, at a noticed meeting that is
recorded and cablecast. That is a public proceeding and a public record, and this
project reports it as one, the same way a local newspaper does. Reducing a
speaker to initials would not protect anyone whose name is already in the
recording, the minutes and the broadcast; it would only make the page harder to
check against the source.

**The risk is not that they are named. It is that they might be named wrongly.**
Everything this project owes a private resident follows from that, and the
protections are therefore accuracy controls rather than anonymity:

1. **Attribution is marked, not asserted.** Where the evidence for a speaker's
   identity is thin, and it usually is thinnest for someone who speaks at one
   meeting and never again, the page says so rather than presenting a confident
   label. The `Diarized As` column in the dialogue CSV preserves the original
   anonymous label so any attribution can be traced back and disputed.

2. **Quotations are machine-checked against the transcript.** Automatic speech
   recognition in this corpus is error-prone in documented, recurring ways. A
   garbled line that turns something harmless into an accusation is this
   project's error, not the district's, and the quote audit exists to catch it.
   Corrections inside quotations appear in square brackets. Read the linked
   timestamp before treating any quotation as verbatim.

3. **A legal-concern flag is never about a private resident.** Flags address the
   conduct of the public body: what it noticed, how it voted, what it sealed,
   whether it followed the statute. A member of the public appears inside a flag
   only as a quoted characterization, labeled as one. This is a rule of the
   project, not a matter of editorial taste, and a page that flags a resident's
   conduct against a statute is a defective page and should be reported as such.

4. **Removal on request.** A private individual who asks to have their name taken
   off a page will have it taken off, without argument and without being asked
   why. This applies to members of the public, not to officials acting in their
   official capacity.

**One thing these controls do not fix.** Speaking for three minutes in a room of
forty people is different from being permanently indexed and machine-summarized
years later, even when every individual fact is public. Aggregating public
records changes what they do, and this project is an aggregation of public
records. That is the reason for the removal promise above, and the reason it is
offered without conditions.

## Corrections

Accuracy matters more to this project than any individual page does.

* **Open an issue** on this repository describing the error, the page it appears
  on, and, where possible, the timestamp in the recording that shows the correct
  fact.
* Corrections to matters of fact will be made and the page will note that it was
  corrected and when.
* Requests to remove a private individual's name will be acted on
  without requiring a reason.
* Officials and bodies whose proceedings are covered here are invited to submit
  corrections on the same footing as anyone else, and their submissions will be
  published alongside the correction.

If you would rather not use a public issue, contact the maintainer directly.

## Where this notice must appear

Every generated page carries the short form of this notice, injected by
`Output/HTML/style.css`. That injection is a required feature of the output, not
a style choice. A build that renders pages without it is a defective build.
