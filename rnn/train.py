from rnn.model import Model
import os
import tensorflow as tf
import rnn.common as common


class Train(Model):

    def __init__(self, config):
        with tf.Graph().as_default(), tf.device(config.train.device):
            super().__init__(config.checkpoint_dir)
            self.MODE = 'TRAIN'
            self.summary_path = os.path.join(config.summaries, 'train')
            self.logger = config.logger
            self._step = 0
            self.max_steps = config.train.steps
            self.inputfile = config.train.inputfile
            self.build(
                config,
                config.train.batch_size,
                keep_prob=config.train.keep_prob)

    def step(self):
        res = self.sess.run([
            self.summary_op,
            self.loss,
            self.accuracy,
            self.precision,
            self.recall,
            self.tvars,
            self.optimizer,
            self.y,
            self.rounded_predictions,
            self.accuracy_2,
            self.global_step])
        self._step = res[-1]
        self.logger.info('{} loss={}, accuracy={}'.format(self.MODE, res[1], res[2]))
        self.logger.info('{} accuracy_2={}'.format(self.MODE, res[9]))
        self.logger.info('{} precision={}, recall={}'.format(self.MODE, res[3], res[4]))
        self.logger.info('{} global_step={}'.format(self.MODE, res[-1]))

        metric = {
            'accuracy': res[2],
            'accuracy_2': res[9],
            'loss': res[1],
            'precision': res[3][0],
            'recall': res[4][0],
            'f1': common.f1(res[3][0], res[4][0])}
        self.summarize(metric)
        return res

    def flush(self):
        self.summary_writer.flush()

    def summarize(self, metric):
        self.summary_writer.add_summary(
            self.as_summary(metric),
            global_step=self._step)
        self.summary_writer.flush()
