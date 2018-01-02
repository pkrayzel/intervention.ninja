rm -rf dist
mkdir dist
cp -rf ~/hw/lib/python3.6/site-packages/* dist
cp ../src/__init__.py dist/.
cp ../src/intervention_ninja.py dist/.
cp -rf ../src/services dist
cd dist && zip -r ../lambda_dist.zip . && cd ..

aws s3 cp --region us-east-1 lambda_dist.zip s3://intervention-ninja-deployment-support/

aws lambda update-function-code --profile private_developer --region us-east-1 --function-name intervention_ninja_email_sender --s3-bucket intervention-ninja-deployment-support --s3-key lambda_dist.zip --publish