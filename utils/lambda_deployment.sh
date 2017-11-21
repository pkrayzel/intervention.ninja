rm -rf dist
mkdir dist
cp -rf ~/ninja/lib/python3.6/site-packages/* dist
cp src/__init__.py dist/.
cp src/intervention_ninja_lambda.py dist/.
cp -rf src/services dist/.
cd dist && zip -r ../dist.zip . && cd ..

aws s3 cp dist.zip s3://deploymentsupport/www.intervention.ninja/

aws lambda update-function-code --function-name intervention_ninja_lambda --s3-bucket deploymentsupport --s3-key www.intervention.ninja/dist.zip --publish