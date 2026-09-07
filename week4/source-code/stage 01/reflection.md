What did you build before using AI? 

a working program that has a list of dictionaries with book_appoinment() and display_appointments() functions, one check that rejects a blank paitent name and an input() flow that books a new appoinment while the program runs 

what did AI help you understand? 
AI reviewed that exact code and named three gaps I hadn't fully worked out: no validation on gp name or time, no check for double booking and that appoinment_time is a plain string, so it can't be stored or checked as real data.

did AI make assumptions? 
fewered then expected. When it made its own version in Part D, it stuck the the brief outline and didn't create extra fields.

how did you verify the AI output?
by running it directly, not just reading and trusting it. I called its functions wit hte same dge cases i used on my own program, a blank name, a duplicate booking and none vlaues. 

what engineering work remained for you?
the AI/s own questions forced this out, where "if not paitent_name" catches a name of just spaces and that a duplicate check must run before a new appoinment is booked not after. using that logic I talked about how this change can be made in part G. AI can help prompt and work with me but not do the work for me as it still left areas to be worked on. 
