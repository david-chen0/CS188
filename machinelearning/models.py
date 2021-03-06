import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        prediction = nn.as_scalar(self.run(x))
        if prediction >= 0:
            return 1
        return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        while True:
            numWrong = 0
            for x, y in dataset.iterate_once(1):
                prediction = self.get_prediction(x)
                if prediction != nn.as_scalar(y):
                    numWrong += 1
                    self.w.update(x, nn.as_scalar(y))

            if numWrong == 0:
                break


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.targetLoss = 0.01 # Spec requires 0.02 but better to be safe
        self.batchSize = 5 # Total size of dataset must be divisible by batch size, 5 seems to work well
        self.learningRate = 0.002 # Learning rate should be between 0.001 and 1.0, <=0.005 seems to work well

        size = 64 # Size should be between 10 and 400, >64 takes too long to converge and <64 is inaccurate

        # Use 1-3 hidden layers
        self.w1 = nn.Parameter(1, size)
        self.b1 = nn.Parameter(1, size)
        self.w2 = nn.Parameter(size, 1)
        self.b2 = nn.Parameter(1, 1)

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        firstLayer = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        secondLayer = nn.AddBias(nn.Linear(firstLayer, self.w2), self.b2)
        return secondLayer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            totalLoss = 0
            totalCount = 0
            for x, y in dataset.iterate_once(self.batchSize):
                loss = self.get_loss(x, y)
                totalLoss += nn.as_scalar(loss)
                totalCount += 1
                gradient = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2])

                self.w1.update(gradient[0], -1 * self.learningRate)
                self.b1.update(gradient[1], -1 * self.learningRate)
                self.w2.update(gradient[2], -1 * self.learningRate)
                self.b2.update(gradient[3], -1 * self.learningRate)

            if totalLoss / totalCount < self.targetLoss:
                break
                

                


class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.targetThreshold = 0.98 # Spec requires 0.97 but better to be safe
        self.batchSize = 1
        self.learningRate = 0.005 # Learning rate should be between 0.001 and 1.0, need a higher learning rate here

        # Bad size combos: (128, 64), (100, 50), 
        size1 = 256
        size2 = 128

        # One hidden layer gets stuck at 95% accuracy, so use 2-3
        self.w1 = nn.Parameter(784, size1)
        self.b1 = nn.Parameter(1, size1)
        self.w2 = nn.Parameter(size1, size2)
        self.b2 = nn.Parameter(1, size2)
        self.w3 = nn.Parameter(size2, 10)
        self.b3 = nn.Parameter(1, 10)


    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        firstLayer = nn.ReLU(nn.AddBias(nn.Linear(x, self.w1), self.b1))
        secondLayer = nn.ReLU(nn.AddBias(nn.Linear(firstLayer, self.w2), self.b2))
        thirdLayer = nn.AddBias(nn.Linear(secondLayer, self.w3), self.b3)
        return thirdLayer

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batchSize):
                loss = self.get_loss(x, y)
                gradient = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])

                self.w1.update(gradient[0], -1 * self.learningRate)
                self.b1.update(gradient[1], -1 * self.learningRate)
                self.w2.update(gradient[2], -1 * self.learningRate)
                self.b2.update(gradient[3], -1 * self.learningRate)
                self.w3.update(gradient[4], -1 * self.learningRate)
                self.b3.update(gradient[5], -1 * self.learningRate)
            
            if dataset.get_validation_accuracy() > self.targetThreshold:
                break


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.targetThreshold = 0.85
        self.batchSize = 32
        self.learningRate = 0.025 # Learning rate should be between 0.001 and 1.0

        # Bad sizes: 
        size = 512

        self.w1 = nn.Parameter(self.num_chars, size)
        self.b1 = nn.Parameter(1, size)
        self.w2 = nn.Parameter(size, size)
        self.b2 = nn.Parameter(1, size)
        self.w3 = nn.Parameter(size, 5)
        self.b3 = nn.Parameter(1, 5)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        result = nn.ReLU(nn.AddBias(nn.Linear(xs[0], self.w1), self.b1))
        for char in xs[1:]:
            # All methods are pretty slow to converge, might be able to improve with another layer?

            # 85%
            result = nn.ReLU(nn.AddBias(nn.Add(nn.AddBias(nn.Linear(char, self.w1), self.b1), nn.Linear(result, self.w2)), self.b2))

            # 80%
            #result = nn.AddBias(nn.Add(nn.AddBias(nn.Linear(char, self.w1), self.b1), nn.Linear(result, self.w2)), self.b2)

            # 80%
            #result = nn.AddBias(nn.Linear((nn.Add(nn.AddBias(nn.Linear(char, self.w1), self.b1), result)), self.w2), self.b2)

            # 79%
            #result = nn.Add(nn.AddBias(nn.Linear(char, self.w1), self.b1), nn.AddBias(nn.Linear(result, self.w2), self.b2))
        return nn.AddBias(nn.Linear(result, self.w3), self.b3)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batchSize):
                loss = self.get_loss(x, y)
                gradient = nn.gradients(loss, [self.w1, self.b1, self.w2, self.b2, self.w3, self.b3])

                self.w1.update(gradient[0], -1 * self.learningRate)
                self.b1.update(gradient[1], -1 * self.learningRate)
                self.w2.update(gradient[2], -1 * self.learningRate)
                self.b2.update(gradient[3], -1 * self.learningRate)
                self.w3.update(gradient[4], -1 * self.learningRate)
                self.b3.update(gradient[5], -1 * self.learningRate)
            
            if dataset.get_validation_accuracy() > self.targetThreshold:
                break
