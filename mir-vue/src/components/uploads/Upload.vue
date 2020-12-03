<template>
 <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="onFileChange()"/>
      </label>
     <v-btn small color="primary" v-on:click="submit()">Primary</v-btn>
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
                
                formData.append('policy',policy)
                formData.append('AWSAccessKeyId',access_key)
                formData.append('signature',signature)
                formData.append('key',key)
                formData.append('file',file)

          

                axios.put(presignedURL, formData)
                // axios.put(parsed_presigned_url, formData, {
                //   headers: {
                //     'Content-Type':'image/png',
              
                //   }
                // });

            }catch(err){
                console.log(err)
            }
        },

        async upload_file(){
            await this.fetch_presigned_url(file)
        },

        submit(){
          this.upload_file()
        },

        onFileChange(){
          this.file = this.$refs.file.files[0]
          console.log()
          
        }
   },
}
</script>