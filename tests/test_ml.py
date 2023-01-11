from lib.ml import Model 
import os.path

def test_train_and_persist(db, seed_training_data, app):
    # Use all data we have on first train.
    # train on all but 1. And use random 1 to ensure it's the same randomness seed 
    # on each call.
    model_name = app.config["MODEL_URL"]
    x_train, x_test, y_train, y_test = Model.get_training_data(random_state=1)
    model = Model.load()
    model.train(x_train, y_train)

    input = [ 3, 14, 14]
    prediction = model.predict([input])
    assert 0 < prediction < 4
    score = model.score(x_test, y_test)
    assert -8 < score < 8
    
    model.persist()
    model.log(score)

    latest_training_log = db.latest_training_log(model_name)
    assert latest_training_log["score"] == score
    assert os.path.isfile(model_name)