$buckets = aws s3api list-buckets --query 'Buckets[*].Name' --output text --profile PROFILE --region REGION
$bucketsArray = $buckets -split '\s+'

foreach ($bucket in $bucketsArray) {
    Write-Host "Checking bucket: $bucket"
    $acl = aws s3api get-bucket-acl --bucket $bucket --query 'Grants[?Grantee.URI==`"http://acs.amazonaws.com/groups/global/AllUsers"`].Permission' --output text --profile PROFILE --region REGION
    if ($acl) {
        Write-Host "Bucket $bucket is publicly accessible via ACL"
    }
    $policy = aws s3api get-bucket-policy --bucket $bucket --query 'Policy' --output text --profile alpha --region eu-west-1 2>&1 | Select-String -Pattern "Allow"
    if ($policy) {
        Write-Host "Bucket $bucket has a policy allowing public access"
    }
}
