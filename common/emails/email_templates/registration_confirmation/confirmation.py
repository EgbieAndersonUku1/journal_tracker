

EMAIL_CONFIRMATION_TEXT = """

Hi {},

Thank you registering JobTracker the one place where you can
consolidate all your job searches in one place. Once you confirm your
email you be able to:


1) Track all your job searches whether it is from Reeds, Linkedln, JobSite, etc
2) Track all your interviews, job outcomes, etc
3) Add your job to the application using an easy to use User interface
4) Write, edit, delete or modify your journal
5) And so much more


--------------------------------------------------------------------------
Copyright jobjournalTracker 2020


"""

EMAIL_CONFIRMATION_HTML = """

<!DOCTYPE html>
<html lang="en" dir="ltr">


<body>


  <div class="container">


    <div class="row">


    <div class="col-lg-9">
      <div class="intro">
        <p class="lead">
          Hi, {},
        </p>

        <p class="lead">

           Thank you registering JobTracker the one place where you
           consolidate all your job searches in one place. Once you confirm your
           email you be able to:
         </p>


         <br>

        <p class="lead"> 1) Track all your job searches whether it is from Reeds, Linkedln, JobSite, etc</p>
         <p class="lead">2) Track all your interviews, job outcomes, etc</p>
         <p class="lead">3) Add your job to the application using an easy to use User interface</p>
         <p class="lead">4) Write, edit, delete or modify your journal</p>
         <p class="lead">5) And so much more</p>

         <br>
         <div class="link">
           Click the link below to confirm your registration <a href="{}/{}/confirm/{}">Click here</a>
         </div>
         
         <br>
         <br>
         <div class="footer">
           Copyright jobjournalTracker 
         </div>

      </div>


    </div>




  </div>

</body>

</html>

"""