# doc-class
### Webservice with training, development CSV uploads

I deployed on AWS EC2 (Ubuntu) a [webservice](https://ec2-18-222-104-42.us-east-2.compute.amazonaws.com/) with training, development CSV uploads[^fn1]. it looks like the following: initially,
<img src="README_resources/index_origin.png" width="600">

and after uploading DEV/TEST CSV file:
<img src="README_resources/index_result.png" width="600">

where two confusion matrices should be (and eventually I failed to do so) displayed as <img src="doc_class/app/templates/images/devconfusion.png" width="300"> <img src="doc_class/app/templates/images/confusion.png" width="300">.

### References


[^fn1] Li, Yezheng, Mar. 12th-14th, 2018, Webservice with training, development CSV uploads, http://ec2-18-222-104-42.us-east-2.compute.amazonaws.com/

[^fn2] Thompson, Ben, Mar 2015, Setting Up Flask on AWS, http://bathompso.com/blog/Flask-AWS-Setup/

[^fn3] Long, Pete, July 2017, Nginx Error – 413 Request Entity Too Large, https://www.petenetlive.com/KB/Article/0001325

### Initial setup for deployment on AWS EC2 (Ubuntu)







### Measurement Criteria

  1. Does your webservice work?
  1. Is your hosted model as accurate as ours? Better? (think confusion matrix)
  1. Your code, is it understandable, readable and/or deployable?
  1. Do you use industry best practices in training/testing/deploying?
  1. Do you use modern packages/tools in your code and deployment pipeline like [this](https://stelligent.com/2016/02/08/aws-lambda-functions-aws-codepipeline-cloudformation/)?
  1. The effectiveness of your demo, did you frame the problem and your approach to a solution, did you explain your thinking and any remaining gaps, etc?
  1. Are we able to run your testcases against your webservice? Can we run them against our webservice?
