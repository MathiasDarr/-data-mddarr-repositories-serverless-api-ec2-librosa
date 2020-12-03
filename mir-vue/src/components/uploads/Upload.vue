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

        async fetch_presigned_url(file){
            try{
                // var url = window.__runtime_configuration.apiEndpoint + '/categories'
                var url ='https://q2pyn2t2s9.execute-api.us-west-2.amazonaws.com/v1/signedURL'
                
                var body = {fileName:'profile_picture.png'}
                const response = await axios.post(url, body)

    
                // var policy = response.data.body.policy
      
                var parsed_body = JSON.parse(response.data.body)
                var parsed_presigned = parsed_body.presigned
  
                var presignedURL = parsed_presigned.url
                var signature = parsed_presigned.fields.signature
                var policy = parsed_presigned.fields.policy
                var access_key = parsed_presigned.fields.AWSAccessKeyId
                var key = parsed_presigned.fields.key

                const formData = new FormData();
                formData.append('file',file)
                formData.append('policy',policy)
                formData.append('AWSAccessKeyId',access_key)
                formData.append('signature',signature)
                formData.append('key',key)
                
                var parsed_presigned_url = presignedURL + key +''

                console.log(parsed_presigned_url)
                axios.put(parsed_presigned_url, formData, {
                  headers: {
                    'Content-Type':'image/png',
                    'x-amz-algorithm':'AWS4-HMAC-SHA256',

                  }
                });

            }catch(err){
                console.log(err)
            }
        },

        async upload_file(){
            await this.fetch_presigned_url(file)
        },

        submit(){
          console.log(this.file)
        },

        onFileChange(){
          this.file = this.$refs.file
          console.log()
          this.submit()
        }
   },
}
</script>