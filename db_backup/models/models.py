import time
import logging
from odoo import models, fields, api
from odoo.addons.db_backup.upload_api.graph_api import get_folder_id, upload_file
from odoo.addons.db_backup.upload_api.download import download_file, trigger_download


_logger = logging.getLogger(__name__)


class db_backup(models.Model):
    _name = 'db_backup.db_backup'
    _description = 'db_backup.db_backup'

    @api.depends('value')
    def backup_db(self):
        try:
            trigger_result = trigger_download()
            if trigger_result['status'] == "success":
                _logger.info['payload']
                time.sleep(600)
                download_result = download_file()
                if download_result['status'] == "success":
                    filename = download_result['payload']
                    _logger.info(
                        "XXXXXXXXX   Uploading to one drive XXXXXXXXX")
                    folder_id = get_folder_id()
                    upload_result = upload_file(folder_id, filename)
                    if upload_result['status'] == 'success':
                        _logger.info(
                            f" WWWWWWWWWWWW done uploading WWWWWWWWWWWWWW")
                    else:
                        _logger.info(
                            f" WWWWWWWWw Failed : {upload_result['reason']} WWWWWWWWWWWWWWWW")
                else:
                    _logger.info(download_result["payload"])
            else:
                _logger.info(trigger_result["payload"])
        except Exception as e:
            _logger.info(e)
            exit(1)
