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


        async fetch_presigned_url(){
            try{
                // var url = window.__runtime_configuration.apiEndpoint + '/categories'
                var url ='https://q2pyn2t2s9.execute-api.us-west-2.amazonaws.com/v1/signedURL'
                // var headers = {
                //     { headers: {'Access-Control-Allow-Origin':'*'}
                // }
                
                var body = {fileName:'profile_picture.png'}
                // const response = await axios({url:url, method: 'post', data: body, headers:{'Access-Control-Allow-Origin':'*'}})
                const response = await axios.post(url,body)

                console.log("no response")
                console.log(response)                

            }catch(err){
                console.log(err)
            }
        },

        async upload_file(){
            await this.fetch_presigned_url()
        },

        onFileChange(){

            this.upload_file()
        }
   },
}
</script>