<template>
 <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="onFileChange()"/>
      </label>
    </div>
  </div>
</template>


<script>
/* eslint-disable */
import axios from 'axios';

export default {
  props: ['files'],
  data () {
    return {
      file: ''
    }
  },
  methods: {
      upload(){
        var albumBucketName = "BUCKET_NAME";
        var bucketRegion = "us-west-2";
        var IdentityPoolId = "IDENTITY_POOL_ID";

        AWS.config.update({
            region: bucketRegion,
                credentials: new AWS.CognitoIdentityCredentials({
                IdentityPoolId: IdentityPoolId
            })
        });

        var s3 = new AWS.S3({
            apiVersion: "2006-03-01",
            params: { Bucket: albumBucketName }
        });
      },


        async fetch_presigned_url(file){
            try{
                // var url = window.__runtime_configuration.apiEndpoint + '/categories'
                var url ='https://q2pyn2t2s9.execute-api.us-west-2.amazonaws.com/v1/signedURL'
                
                var body = {fileName:'profile_picture.png'}
                const response = await axios.post(url, body)

                     

                // var policy = response.data.body.policy
      
                var parsed_body = JSON.parse(response.data.body)
                var parsed_presigned = parsed_body.presigned
                console.log(parsed_body.presigned.fields)
                var presignedURL = parsed_presigned.url
                console.log(presignedURL)
                var signature = parsed_presigned.fields.signature
                console.log(signature)
                // var presignedURL = parsed_presigned.url
                // var access_key = parsed_presigned.AWSAccessKeyId
                // var key = parsed_presigned.key
                // var policy = parsed_presigned.policy
                // var signature = parsed_presigned.signature

                // // var key = parsed_body.key

    
                // console.log("key") 
                // console.log(key)
                // console.log("signature")          
                // console.log(signature)     
                // console.log(response.data.body)        
                // const formData = new FormData();
                // formData.append('file',file)
                // formData.append('policy',policy)
                // formData.append('AWSAccessKeyId',access_key)
                // formData.append('signature',signature)
                // formData.append('key',key)
                

                // axios.post(presignedURL, formData, {
                //   headers: {
                //     'Content-Type': 'multipart/form-data'
                //   }
                // });

            }catch(err){
                console.log(err)
            }
        },

        async upload_file(){
            await this.fetch_presigned_url(file)
        },

        onFileChange(){
            this.upload_file(file)
        }
   },
}
</script>