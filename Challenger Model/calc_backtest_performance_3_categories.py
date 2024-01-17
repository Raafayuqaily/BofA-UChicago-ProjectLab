import pandas as pd
import sys
import matplotlib.pyplot as plt

def get_accuracy_3cat(result_file_path, require_collapse = False):
    print("------ Calculate Performance of ChatGPT Starts ------")

    data = pd.read_excel(result_file_path)

    # delete error response
    data['Final Score'] = pd.to_numeric(data['Final Score'], errors='coerce')
    data['Score_by_ChatGPT'] = pd.to_numeric(data['Score_by_ChatGPT'], errors='coerce')
    data.dropna(subset=['Score_by_ChatGPT','Final Score'],inplace=True)

    if require_collapse:
        # collapse scores from 1-5 to 1-3
        category_mapping = {1:1, 2:1, 3:2, 5:3, 4:3}
        # Apply the transformation to the specified column
        data['Score_by_ChatGPT'] = data['Score_by_ChatGPT'].replace(category_mapping)
        data['Final Score'] = data['Final Score'].replace(category_mapping)

    # Delete invalid Score
    invalid_score = data[(data['Score_by_ChatGPT'].astype(int) > 3) | (data['Score_by_ChatGPT'].astype(int) < 1)]
    invalid_score_cnt = len(invalid_score)
    print(f"Chatgpt responded with invalid score Total {invalid_score_cnt} times")
    if invalid_score_cnt > 0:
        print(f"Detailed Invalid Scores and Frequency: \n{invalid_score['Score_by_ChatGPT'].value_counts()}")
    
    data = data[(data['Score_by_ChatGPT'].astype(int) <= 3) & (data['Score_by_ChatGPT'].astype(int) >= 1)]

    # calculate Mean Absolute Error (MAE)
    data['Absolute_Error'] = abs(data['Score_by_ChatGPT'] - data['Final Score'])
    MAE = data['Absolute_Error'].mean()
    print(f"Mean Absolute Error = {MAE:.2f} on a scale of 1-3")
    
    # calculate accuracy: exact match
    accuracy_3cat = (((data['Score_by_ChatGPT'] == 1) & (data['Final Score'] == 1)).sum() + ((data['Score_by_ChatGPT'] ==2) & (data['Final Score'] == 2)).sum() + ((data['Score_by_ChatGPT'] == 3) & (data['Final Score'] == 3)).sum()) / len(data)
    print(f"Accuracy Score (3 category) = {accuracy_3cat:.2%}")

    # calculate percentage data accurately rated by ChatGPT in each category
    positive_accuracy = len(data[(data['Final Score'] == 3) & (data['Score_by_ChatGPT'] == 3)]) / len(data[data['Final Score'] == 3])
    print(f"{positive_accuracy:2%} positive news are correctly labeled")
    negative_accuracy = len(data[(data['Final Score'] == 1) & (data['Score_by_ChatGPT'] == 1)]) / len(data[data['Final Score'] == 1])
    print(f"{negative_accuracy:2%} negative news are correctly labeled")
    neutral_accuracy = len(data[(data['Final Score'] == 2) & (data['Score_by_ChatGPT'] == 2)]) / len(data[data['Final Score'] == 2])
    print(f"{neutral_accuracy:2%} neutral news are correctly labeled")

    # calculate percentage data wrongly rated by ChatGPT in each category
    neutral_labeled_positive = len(data[(data['Final Score'] == 2) & (data['Score_by_ChatGPT'] ==3)]) / len(data[data['Final Score'] == 2])
    print(f"{neutral_labeled_positive:2%} neutral news are wrongly labeled as positive by ChatGPT")

    neutral_labeled_negative = len(data[(data['Final Score'] == 2) & (data['Score_by_ChatGPT'] == 1)]) / len(data[data['Final Score'] == 2])
    print(f"{neutral_labeled_negative:2%} neutral news are wrongly labeled as negative by ChatGPT")

    positive_labeled_neutral = len(data[(data['Final Score'] == 3) & (data['Score_by_ChatGPT'] == 2)]) / len(data[data['Final Score'] == 3])
    print(f"{positive_labeled_neutral:2%} positive news are wrongly labeled as neutral by ChatGPT")

    positive_labeled_negative = len(data[(data['Final Score'] == 3) & (data['Score_by_ChatGPT'] == 1)]) / len(data[data['Final Score'] == 3])
    print(f"{positive_labeled_negative:2%} positive news are wrongly labeled as negative by ChatGPT")

    # plot scores distribution histgram
    plt.hist([data['Score_by_ChatGPT'], data['Final Score']], 
             bins=[.5,1.5,2.5,3.5], label=['Score Predicted by Challenger Model','Original Score'])
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.xticks(range(0,4))
    plt.title('Score Predicted by Challenger Model vs. Original Scores')
    plt.legend()
    plt.show()

    # plot mean absolute error distribution histogram
    data['Error'] = data['Score_by_ChatGPT'] - data['Final Score']
    plt.hist(data['Error'], bins=[-2.5,-1.5,-0.5,.5,1.5,2.5],
             label=['Predicted - Actual Score'],
             width=0.95)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.xticks(range(-2,3))
    plt.title('Prediction Error Distribution')
    plt.legend() 
    plt.show()
    
    print("------ Calculate Performance of ChatGPT End ------")


if __name__ == "__main__":
    local = False
    if local:
        # result_file_path = 'chatGPT_model/results/final_scores/sentiment_scores_by_ChatGPT_202311301514.xlsx'
        result_file_path = ''
    else:
        result_file_path = sys.argv[1]

    get_accuracy_3cat(result_file_path)