# Document classification: a quick start
### Webservice with training and DEV/TEST CSV uploads

I deployed on AWS EC2 (Ubuntu) a webservice with training and DEV/TEST CSV uploads[^fn1]. It initially appears
<img src="README_resources/index_origin.png" width="600">

and after uploading DEV/TEST CSV file:
<img src="README_resources/index_result.png" width="600">

where two confusion matrices should be displayed as (and eventually I failed to display the two due to html's issue of locating images) : 
<p> <img src="doc_class/app/templates/images/devconfusion0.png" width="300"> <img src="doc_class/app/templates/images/confusion0.png" width="300">
</p> 

with overall accuracy ~ 93.8%, saved classifier of size at most 20~40MB (of course depending on training CSV) and original codes are here: [trainNB.ipynb](README_resources/NaivBayes_trigram/trainNB.ipynb) and [loadNB.ipynb](README_resources/NaivBayes_trigram/loadNB.ipynb).
(of course depending on training CSV) and original codes are here:


# Tutorial: for user and for developer
### For user: how to use webservice
1. In a friendly browser, enter [^fn1].
2. Since we have pretrained model in the instance, a user can just ignore two buttons in the first block and upload DEV/TEST CSV (of same format as the original training CSV) by two buttons in the second block of htmls (first block and second block are separated by ------------------------).
3. Once the confusion matrices are shown (since I have problem locating local image files by html, they are presented by two same W3schools' image(s) from an online source), use newly appeared (four) buttons to download predicted labels and PNG for confusion matrix of training CSV and DEV/TEST CSV.
4. (Optional) If one want to change training CSV (the default pretrained model uses entire original CSV) so as to overwrite the pretained/ previous model, use two buttons in the first block.
- If you need to get back to the pretrained model,
- (pretrained by the entire dataset, the classifier is ~44MB, reasonably small)
- notice there is a third button in first block called **Back to original model**.

5. About results and confusion matrices:

- For training dataset (first block), `devresult.csv` are true label/ predicted label's on random sample of one tenth of all training dataset (techinque is the fast reservoir sampling); confusion matrix `devconfusion.png` is the corresponding one.
- For DEV/ TEST dataset (second block), `result.csv` is true label/ predicted label on random sample of one tenth of all training dataset (techinque is the fast reservoir sampling); confusion matrix `confusion.png` is the corresponding one.
6. If you want to run on a **truly** TEST CSV (that is, rather than a DEV CSV which has the true underlying label), maybe you can just label 'A' before every line to follow training CSV's format and then use two buttons in the second block. In this case, ```result.csv``` gives you the predicted labels for TEST CSV; just ignore confusion matrix `confusion.png` since it does not make sense.
7. If you confront HTML page ```502 Bad Gateway``` or ```Method Not Allowed```, it is very likely that you can resolve the issue by going back to enter [^tn1] ended with ```.compute.amazonaws.com``` (rather than ended with subpage notation ```.../train```, ```.../upload```, ```.../OriginalTraining```, ```.../download1```) and do your test of the system from the scratch.

In the extreme case you have to contact me to resolve a bug I have not debugged out beforehand -- however, I do not expect that since I think my instruction 7 include all the cases (instruction 7 may be little bit uncomfortable, but they are not bugs).

### For developer: initial setup for deployment on AWS EC2 (Ubuntu)

1. Establish a AWS EC2 (Ubuntu Server 16.04 LTS (HVM), SSD Volume Type) instance following [^fn2] where the only difference is to choose 't2.small' for enough CPU memory (2GiB). Remember to set inbound rules [^fn2]. Denote IPv4 address of the instance by [EC2-IPv4].
2. Before ssh, it is convenient to edit the `~/.ssh/config` (local machine) by adding [^fn2]
<figure class="highlight"><pre><code class="language-bash" data-lang="bash"><div class="shell"><pre><span></span>Host aws
    HostName <span class="m">[EC2-IPv4]</span>
    User ubuntu
    Port <span class="m">22</span>
    IdentityFile ~/.ssh/aws.pem</code></pre></figure>


3. Run `ssh aws` to log in and `git clone https://github.com/yezhengli-Mr9/doc-class`.
4. We use python27 and need several packages: together with `nginx`, `uwsgi` [^fn2], we run
```
sudo apt-get update
sudo apt-get install python-pip
sudo apt-get install nginx
sudo apt-get install python-tk
sudo apt-get install uwsgi-core uwsgi-plugin-python
pip install --upgrade pip
pip install matplotlib sklearn scipy flask
```
5. In the root (of your EC2 instance), run `sudo cp nginx.conf /etc/nginx/nginx.conf` where `nginx.conf` is updated according to [^tn2, ^tn3]. After this, in order to clean up possible `uwsgi` taking the address localhost:5000 (of the EC2 instance) and restart `nginx`, run 
```
uwsgi --stop ~/doc_class/doc_class.pid
sudo killall -9 uwsgi
sudo /etc/init.d/nginx restart
uwsgi ~/doc_class/uwsgi.ini
```
6. Finally, in a friendly browser, enter [^tn1].

7. For debug, debug the system locally (for example, via `ssh -L 5000:localhost:5000 aws`) before publishing it by AWS.




### Measurement Criteria

**1. Does your webservice work?** Yes.

**2. Is your hosted model as accurate as ours? Better? (think confusion matrix)** The NB model embedded in my webservice refers to ones in[^fn4] but with trigrams and only focus on most frequent (70, 100 or 300) words:
<img src="doc_class/app/templates/images/devconfusion0.png" width="300"> <img src="doc_class/app/templates/images/confusion0.png" width="300">

with overall accuracy ~ 93.8%, saved classifier of size at most ~20-44MB  and original codes here: [trainNB.ipynb](README_resources/NaivBayes_trigram/trainNB.ipynb) and [loadNB.ipynb](README_resources/NaivBayes_trigram/loadNB.ipynb).


**3. Your code, is it understandable, readable and/or deployable?** 

**4. Do you use industry best practices in training/testing/deploying?** No since I do not know the best practices.

**5. Do you use modern packages/tools in your code and deployment pipeline like [this](https://stelligent.com/2016/02/08/aws-lambda-functions-aws-codepipeline-cloudformation/)?** I use EC2.

**6. The effectiveness of your demo, did you frame the problem and your approach to a solution, did you explain your thinking and any remaining gaps, etc?** 
- File loading is time-consuming. 
- Since I managed to make the classifier as small as ~20-44MB while keeping overall accuracy >90%, 
- the original issue is solved.


**7. Are we able to run your testcases against your webservice? Can we run them against our webservice?** Yes. My test cases are in [doc_class/uploads/](doc_class/uploads/) where for example, `row160.csv` includes leading 160 lines of original csv. Upload specification appears in htmls of my webservice, notice
- the larger the size, the longer the time to upload (although a 273MB file is uploadable).
- upload of training CSV is not necessary. 
- You can return to my near-optimal pretrained model by 
- third button **Back to original model** in first block.


### References

[^fn1] Li, Yezheng, Mar. 12th-14th, **21th** 2018, Webservice with training, development CSV uploads, [http://ec2-??-??-??-??.us-east-2.compute.amazonaws.com/](http://ec2-18-216-141-107.us-east-2.compute.amazonaws.com) corresponding to [EC2-IPv4]. 
- I have already established one with [EC2-IPv4] =18.216.141.107 
- with corresponding public DNS http://ec2-18-216-141-107.us-east-2.compute.amazonaws.com
- however, as I mentioned in step 1 of **tutorial for developer**, it is not a free tier, please 
- inform me when you finish reviewing my code and I will stop the current running instance
- (which later on will change its [EC2-IPv4]). 
- Public DNS be made non-dynamic -- just take time and I think it not quite important.  

[^fn2] Thompson, Ben, Mar 2015, Setting Up Flask on AWS, http://bathompso.com/blog/Flask-AWS-Setup/

[^fn3] Long, Pete, July 2017, Nginx Error – 413 Request Entity Too Large, https://www.petenetlive.com/KB/Article/0001325

[^fn4] Shaikh, Javed, July 2017, Machine Learning, NLP: Text Classification using scikit-learn, python and NLTK, https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
