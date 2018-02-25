# TODO parametrize:
# ********************************
# lambda_sns_publisher
# intervention-ninja-sns-publisher
# ********************************
LAMBDA_FUNCTION_NAME_PREFIX="intervention-ninja-"
FILE_NAME_PREFIX="lambda_"
SUFFIX="email-sender"

if [ "$#" -eq 1 ]; then
    SUFFIX=$1
fi

SUFFIX_UPPERCASE="${SUFFIX/-/_}"

LAMBDA_FUNCTION_NAME="$LAMBDA_FUNCTION_NAME_PREFIX$SUFFIX"
FILE_NAME="$FILE_NAME_PREFIX$SUFFIX_UPPERCASE"
VENV="$SUFFIX/lib/python3.6/site-packages/"

echo $LAMBDA_FUNCTION_NAME
echo $FILE_NAME

# create virtual environment with all dependencies
rm -rf $SUFFIX
virtualenv $SUFFIX -p python3
pip install -r ../requirements_$FILE_NAME.txt -t $VENV

# package lambda with dependencies
rm -rf dist
mkdir dist
cp -rf $VENV/* dist
rm -rf ../src/__pycache__
rm -rf ../src/services/__pycache__
cp -r ../src/ dist/.
cd dist && zip -r ../$FILE_NAME.zip . && cd ..

# deploy to s3 bucket
aws s3 cp --region us-east-1 $FILE_NAME.zip s3://intervention-ninja-deployment-support/

# update lambda code through api
aws lambda update-function-code --profile private_developer --region us-east-1 --function-name $LAMBDA_FUNCTION_NAME --s3-bucket intervention-ninja-deployment-support --s3-key $FILE_NAME.zip --publish