/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_recognize_phonemes_recognize_phonemes_post } from '../models/Body_recognize_phonemes_recognize_phonemes_post';
import type { PhonemeRecognitionRequest } from '../models/PhonemeRecognitionRequest';
import type { RecognitionResultSchema } from '../models/RecognitionResultSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Recognize Phonemes
     * @param formData
     * @returns RecognitionResultSchema Successful Response
     * @throws ApiError
     */
    public static recognizePhonemesRecognizePhonemesPost(
        formData: Body_recognize_phonemes_recognize_phonemes_post,
    ): CancelablePromise<RecognitionResultSchema> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/recognize/phonemes',
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Recognize
     * @param requestBody
     * @returns RecognitionResultSchema Successful Response
     * @throws ApiError
     */
    public static recognizeRecognizePhonemeToTextPost(
        requestBody: PhonemeRecognitionRequest,
    ): CancelablePromise<RecognitionResultSchema> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/recognize/phoneme_to_text',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
