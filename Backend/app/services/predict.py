import os
import sys
from google.cloud import storage
from core.errors import PredictException, ModelLoadException
from core.config import MODEL_NAME, MODEL_PATH, MODEL_ABS_PATH, KEY_PATH
import torch.nn.functional as F
import torch
from loguru import logger
import joblib


sys.path.append(MODEL_ABS_PATH)
from HGAT import load_model
from HGAT.args import config

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= KEY_PATH

class MachineLearningModelHandlerScore(object):
    model = None
    user_emb = None
    recipe_emb = None
    ing_emb = None
    interaction = None
    @classmethod
    def predict(cls, u_id, r_id, load_wrapper=None, method="predict"):
        hgat_model, user_emb, recipe_emb, ing_emb, interaction = cls.get_model(load_wrapper)

        print("predict: u_id:{}, r_id:{}".format(u_id, r_id))

        # if hasattr(clf, method):
        #     return getattr(clf, method)(input)
        
        try:
            u_id = int(u_id)
            user_inter = interaction[u_id]

            if r_id == None:
                r_id = []
            else:
                r_id = list(map(int,r_id.split('_')))
                user_inter[r_id] = 1

            if u_id > user_emb.shape[0]:
                print([])
                return str('[]')

            pred = hgat_model(user_emb[[u_id]],[recipe_emb], [interaction[u_id]])
            pred = F.log_softmax(pred, dim=0)
            pred[interaction[u_id]>0] = -1e6
            #return pred.to('cpu').topk(config.topk)
            tensor_out = pred.to('cpu').topk(config.topk)
            out = dict()
            out['values'] = list(tensor_out.values.tolist())
            out['indices'] = list(tensor_out.indices.tolist())
            print("good out")
            return out
        except Exception as e:
            raise PredictException(f"Cannot pred ...")

    @classmethod
    def get_model(cls, load_wrapper):
        if cls.model is None and load_wrapper:
            cls.model, cls.user_emb, cls.recipe_emb, cls.ing_emb, cls.interaction = cls.load(joblib.load)
        return cls.model, cls.user_emb, cls.recipe_emb, cls.ing_emb, cls.interaction

    @staticmethod
    def load(load_wrapper):
        # download
        bucket_name = "https://console.cloud.google.com/storage/browser/recipe_project_bucket"
        source_blob_name = "recipe_Data"
        destination_dir = f"{MODEL_PATH}/HGAT"
        download_blob(bucket_name, source_blob_name, destination_dir)

        model = None
        if MODEL_PATH.endswith("/"):
            path = f"{MODEL_PATH}{MODEL_NAME}"
        else:
            path = f"{MODEL_PATH}/{MODEL_NAME}"
        if not os.path.exists(path):
            message = f"Machine learning model at {path} not exists!"
            logger.error(message)
            raise FileNotFoundError(message)
        model, user_emb, recipe_emb, ing_emb, interaction = load_model.load(load_wrapper)

        # model = load_wrapper(path)
        if not model:
            message = f"Model {model} could not load!"
            logger.error(message)
            raise ModelLoadException(message)
        return model, user_emb, recipe_emb, ing_emb, interaction


def download_blob(bucket_name, source_blob_name, destination_dir):
    """Downloads a blob from the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    
    # The ID of your GCS object
    # source_blob_name = "storage-object-name"

    # The path to which the dir should be downloaded
    # destination_dir = "local/path/to/dir"

    storage_client = storage.Client()

    # bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    for blob in storage_client.list_blobs(os.path.basename(bucket_name)):
        destination_file_name = os.path.join(destination_dir, blob.name)
        blob.download_to_filename(destination_file_name)
        print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            blob.name, bucket_name, destination_file_name
        )
)
